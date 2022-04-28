<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- <div>
      Pipeline ID: {{filePipeline.metadata.pipelineId}}
    </div> -->
    <v-card outlined class="ma-3 pa-3" v-for="(file, key) in filePipeline.metadata.initialFiles" :key="key">
    <div class="title">{{file.name}}</div>    
    <div>Columns: {{file.columns}} x Rows: {{file.rows}}</div>  
    <div></div>    
    <div>Column: 
      <v-chip :color="file.invalidColumns.includes(name) ? 'purple lighten-4' : ''" v-for="(name, key) in file.columnNames" :key="key">
        {{name}}
      </v-chip>
    </div>
      <div v-if="file.invalidColumns.length == 0" class="mt-3">
        <v-icon color="green" >mdi-check-circle</v-icon> No non-numerical columns.

      </div>
      <div v-if="file.invalidColumns.length > 0">
        <div class="pt-3">
          <v-alert color="blue" text dense>
            {{file.invalidColumns.length}} column<span v-if="file.invalidColumns.length > 1">s</span> with non-numerical data that need to be addressed are highlighted in purple 
          </v-alert>
          
        </div>
        <div class="mt-3 overline">Invalid Column Adjustments</div>   
        <v-card flat class="px-2 py-2" v-for="(transform, col) in file.invalidColumnsTransforms" :key="col">
          <div v-if="transform.type == 'mixed_to_numeric'">
            <div><v-chip color="purple lighten-4" class="">{{col}}</v-chip></div>
            <div class="ml-3">This column has predominately numerical data. Non-numerical values will be removed.</div>
            
          </div>
          <div v-if="transform.type == 'category_to_binary'">
            <div><v-chip color="purple lighten-4" class="">{{col}}</v-chip></div>
            <div class="ml-3">This coulmn has two values which will be replaced by a binary representation.</div>
            <v-row class="mt-2 mx-1">
              <v-col cols="3" v-for="(val, cat) in transform.map" :key="cat">
                <div >
                  <v-select outlined dense :label="cat" @change="flipValues($event, cat, col, key)" v-model="transform.map[cat]" :items=[0,1]></v-select>
                </div>            
              </v-col>
            </v-row>
          </div>
          <div v-if="transform.type == 'one_hot_encode'">
            <div><v-chip color="purple lighten-4" class="">{{col}}</v-chip></div>
            <div class="ml-3">This column contains multiple categories. Each category will be given a seperate binary column.</div>
          </div>      
        </v-card>  
      </div>    
  
    </v-card>  
    <div class="text-right" >

      <v-btn
        @click="filePipeline.applyTransforms()"
        class="primary"
        rounded
        text
        dark
        >
        Next Step
      </v-btn>
    </div>    

  </v-card>
</template>
<script>
//packages

//support code

//components
import StepHeading from '@/components/StepHeading'

//Inspired by: https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
export default {
  name: 'StepFileDrop',
  components: {
    StepHeading
  },
  data() {
    return {

    }
  },
  props: [
    'filePipeline',
    'stepNumber',
    'stepTitle',
  ],
  watch: {
    filePipeline() {
      console.log(this.filePipeline)

    }
  },
  methods: {
    flipValues(val, cat, col, file) {
      let map = this.filePipeline.metadata.initialFiles[file].invalidColumnsTransforms[col].map
      for (let i in map) {
        if (i == cat) {
          map[i] = val
        }
        else {
          map[i] = Math.abs(val - 1)
        }
      }
    },
  }
}
</script>
