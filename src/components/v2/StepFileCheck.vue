<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- <div>
      Pipeline ID: {{filePipeline.metadata.pipelineId}}
    </div> -->
    <v-card flat class="my-2" v-for="(file, key) in filePipeline.metadata.initialFiles" :key="key">
    <div class="overline primary--text">{{file.name}}</div>      
      <div v-if="file.invalidColumns.length == 0" class="mt-3 ml-3">
        <v-icon color="green" >mdi-check-circle</v-icon> No non-numerical columns.
      </div>
      <div class="ml-4" v-if="file.invalidColumns.length > 0">
        <div class="">
          <div>
            {{file.invalidColumns.length}} column<span v-if="file.invalidColumns.length > 1">s</span> with non-numerical data that need to be addressed are highlighted 
          </div>
          <v-chip class="mt-2" small :color="file.invalidColumns.includes(name) ? 'purple lighten-4' : ''" v-for="(name, key) in file.columnNames" :key="key">
            {{name}}
        </v-chip>          
        </div> 
        <v-card flat class="py-2" v-for="(transform, col) in file.invalidColumnsTransforms" :key="col">
          <div v-if="transform.type == 'mixed_to_numeric'">
            <div>
              <span class="purple--text">{{col}}</span>
              <span class="ml-3 caption" >This column has predominately numerical data. Non-numerical values will be removed.</span>
            </div>
          </div>
          <div v-if="transform.type == 'one_hot_encode'">
            <div>
              <span class="purple--text">{{col}}</span>
              <span class="ml-3 caption" >This column contains multiple categories. Each category will be given a seperate binary column.</span>
            </div>
            <div class="ml-3"></div>
          </div>      
        </v-card>  
      </div>    
  
    </v-card>  
    <div class="text-right" >
      <v-btn
        @click="filePipeline.applyTransforms()"
        class="primary"
        :disabled="disableNext"
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
    'disableNext'
  ],
  watch: {
    filePipeline() {
      console.log(this.filePipeline)

    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },  
  methods: {

  }
}
</script>
