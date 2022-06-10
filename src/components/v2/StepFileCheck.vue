<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- <div>
      Pipeline ID: {{filePipeline.metadata.pipelineId}}
    </div> -->

 <v-card flat outlined class="pa-3 my-2" v-for="(file, index) in filePipeline.files" :key="index">
      <v-row dense >
        <v-col cols="6">
          <v-icon>mdi-wrench</v-icon>
          {{ file.name }}
        </v-col>
        <v-col cols="6">
          <div v-if="filterRemovedColumns(file.invalidColumns, filePipeline.columnsToRemove).length == 0" class="mt-3 ml-3">
              <v-icon color="green" >mdi-check-circle</v-icon> No non-numerical columns.
            </div>
            <div class="ml-4" v-if="filterRemovedColumns(file.invalidColumns, filePipeline.columnsToRemove).length > 0">
              <div class="">
                <div>
                  {{filterRemovedColumns(file.invalidColumns, filePipeline.columnsToRemove).length}} column<span v-if="filterRemovedColumns(file.invalidColumns, filePipeline.columnsToRemove).length > 1">s</span> with non-numerical data 
                </div>         
              </div> 
              <v-card flat class="py-2" v-for="(transform, col) in file.invalidColumnsTransforms" :key="col">
                <div v-if="!filePipeline.columnsToRemove.includes(col)">
                  <div v-if="transform.type == 'mixed_to_numeric'">
                    <div>
                      <v-chip color="purple" dark>{{col}}</v-chip>
                      <span class="ml-3 " >Predominately numerical data. Non-numerical values will be removed.</span>
                    </div>
                  </div>
                  <div v-if="transform.type == 'one_hot_encode'">
                    <div>
                      <v-chip color="purple" dark>{{col}}</v-chip>
                      <span class="ml-3 " >Each category will be given a seperate binary column.</span>
                      <div v-if="transform.unique_values.length >= 20">
                        <v-alert class="my-4" text color="purple">This column has {{transform.unique_values.length}} unique values. We recommend removing the column due potentially detrimental expansion of dataset.</v-alert>
                        <v-select
                          label="Action"
                          outlined 
                          dense  
                          :items="generateDropdownOptions(transform)"
                          item-value="value"
                          item-text="text" 
                          v-model="transform.keep_column"></v-select>
                      </div>
                    </div>
                    <div class="ml-3"></div>
                  </div>                     

                </div>
   
              </v-card>  
            </div>              
        </v-col>
      </v-row>
    </v-card>
    <div class="text-right" >
      <v-btn
        @click="$emit('nextStep')"
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

    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },
  computed: {

  },
  methods: {
    filterRemovedColumns(listOfInvalidColumns, columsnToRemove) {
      return listOfInvalidColumns.filter(item => {
        return !columsnToRemove.includes(item)
      })
    },
    generateDropdownOptions(transform) {
      return [
        {
          text: 'Covert to ' + transform.unique_values.length + ' columns',
          value: true
        },
        {
          text: 'Remove Column',
          value: false
        }
      ]
    },
    

  }
}
</script>
