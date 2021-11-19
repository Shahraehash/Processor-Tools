<template>
  <v-card
    outlined
    class="ma-3 pa-5"
  >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />

    <div>

      <v-card outlined class="ma-5 pa-3">
        <div class="overline">
          {{fileName}}
        </div>
        <v-layout class="ml-5">
          <v-row>
            <v-col cols="6" >
              <v-select
                outlined
                dense
                label="Data Set Type"
                v-model="fileObject.dataSet"
                :items="$store.state.dataSet"
                item-text="name"
                item-value="value"
              ></v-select>
              <v-file-input
                v-model="fileObject.file"
                prepend-icon="mdi-file"
                chips
                truncate-length="100"
                outlined
                :disabled="fileObject.dataSet == null"
                :label="fileObject.dataSet + ' file'"
                @change="fileObject.dataFileUpload()"
              ></v-file-input>
            </v-col>
            <v-col cols="6" class="text-center">
              <v-progress-circular color="blue" size="50" width="10" v-if="fileObject.uploading" indeterminate></v-progress-circular>
              <DataValidation
                class="mt-n3"
                :fileData="fileObject.fileMetadata"
                :dataType="fileObject.dataSet"
                @dataValid="fileValidationSet"
              />
            </v-col>
          </v-row>
        </v-layout>
        <v-expansion-panels
          class="pa-5"
          v-if="fileObject.fileMetadata"
          >
          <v-expansion-panel
            dark
          >
            <v-expansion-panel-header>
              View Data Descriptions
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-data-table
                :headers="[
                  {text: 'Column', value:'feature'},
                  {text: 'Count', value:'count'},
                  {text: 'Mean', value:'mean'},
                  {text: 'STDEV', value:'std'},
                  {text: 'Min', value:'min'},
                  {text: '25%', value:'25%'},
                  {text: '50%', value:'50%'},
                  {text: '75%', value:'75%'},
                  {text: 'Max', value:'max'},
                  {text: 'Skew', value:'skew'},
                  ]"
                :items="fileObject.fileMetadata.describe"
                class="elevation-1"
              >
              </v-data-table>

            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card>
    </div>

  </v-card>

</template>
<script>
import StepHeading from '@/components/StepHeading'
import DataValidation from '@/components/DataValidation'

export default {
  name: 'FileUploadSingle',
  components: {
    StepHeading,
    DataValidation
  },
  props: [
    'stepNumber', //StepHeading component
    'stepTitle', //StepHeading component
    'fileObject',
    'fileName'
  ],
  data() {
    return {
    }
  },
  methods: {
    //Receives $emit from DataValidation component
    fileValidationSet(validation) {
      this.fileObject.fileValidation = validation
    }
  }
}
</script>
