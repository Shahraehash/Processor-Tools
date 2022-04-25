<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div>
      Pipeline ID: {{filePipeline.metadata.pipelineId}}
    </div>
    <v-card outlined class="ma-3 pa-3" v-for="(file, key) in filePipeline.metadata.initialFiles" :key="key">
    <div>{{file.name}}</div>    
    <div>Columns: {{file.columns}}</div>  
    <div>Rows: {{file.rows}}</div>    
    <div>Column Names: {{file.columnNames}}</div>    
    <div>Invalid Column Adjustments</div>    
    <v-card outlined class="ma-2 pa-2" v-for="(transform, col) in file.invalidColumnsTransforms" :key="col">
      {{col}}

      <div v-if="transform.type == 'mixed_to_numeric'">
        {{transform.type}}
      </div>
      <div v-if="transform.type == 'category_to_binary'">
        {{transform.type}}


        <v-row>
          <v-col cols="3" v-for="(val, cat) in transform.map" :key="cat">
            <div >
              <v-select outlined dense :label="cat" @change="flipValues($event, cat, col, key)" v-model="transform.map[cat]" :items=[0,1]></v-select>
            </div>            
          </v-col>
        </v-row>
        
    

        
    
      </div>
        
      <div v-if="transform.type == 'one_hot_encode'">
        {{transform.type}}

      </div>      
    </v-card>    
    </v-card>  



    <div class="text-right" >
      <v-btn
        @click="applyTransforms()"
        class="primary"
        rounded
        text
        dark
        >
        Dummy Encode
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
    applyTransforms() {
      this.filePipeline.applyTransforms()
    }
      



  }
}
</script>
