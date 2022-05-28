<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- <div>
      Pipeline ID: {{filePipeline.metadata.pipelineId}}
    </div> -->

 <v-card flat outlined class="pa-3 my-2" v-for="(file, index) in filePipeline.metadata.initialFiles" :key="index">
      <v-row dense >
        <v-col cols="6">
          <v-icon>mdi-wrench</v-icon>
          {{ file.name }}
        </v-col>
        <v-col cols="6">
          <div v-if="file.invalidColumns.length == 0" class="mt-3 ml-3">
              <v-icon color="green" >mdi-check-circle</v-icon> No non-numerical columns.
            </div>
            <div class="ml-4" v-if="file.invalidColumns.length > 0">
              <div class="">
                <div>
                  {{file.invalidColumns.length}} column<span v-if="file.invalidColumns.length > 1">s</span> with non-numerical data 
                </div>         
              </div> 
              <v-card flat class="py-2" v-for="(transform, col) in file.invalidColumnsTransforms" :key="col">
                <div v-if="transform.type == 'mixed_to_numeric'">
                  <div>
                    <v-chip>{{col}}</v-chip>
                    <span class="ml-3 " >Predominately numerical data. Non-numerical values will be removed.</span>
                  </div>
                </div>
                <div v-if="transform.type == 'one_hot_encode'">
                  <div>
                    <v-chip>{{col}}</v-chip>
                    <span class="ml-3 " >Each category will be given a sepertae binary column.</span>
                  </div>
                  <div class="ml-3"></div>
                </div>      
              </v-card>  
            </div>              


        </v-col>
      </v-row>
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
