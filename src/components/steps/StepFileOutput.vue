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
      <v-layout>
        <v-row>
          <v-col cols="6">
            <v-card class="px-3 py-1 mt" flat outlined>
              <div class="overline">
                Output Summary
              </div>
              <div>
                <div v-if="loadingFileData">
                  <v-progress-circular color="blue" size="50" width="10" indeterminate></v-progress-circular>

                </div>
                <div v-if="!loadingFileData">
                  <div>
                    Total Output Columns: {{outputList + 1}} (including target)
                  </div>
                  <div>
                    Feature Columns: {{outputList}} of {{file0.featureList.length}} original
                  </div>
                  <div>
                    Target Column: {{file0.target}}
                  </div>
                  <div>
                    First File Rows Total: {{file0.fileMetadata.rows}}
                  </div>
                  <div>
                    First File Rows Used: {{file0.fileMetadata.rows - file0.correlationOutputFiles.missing_count}}
                  </div>
                  <div>
                    First File Rows Missing Data: {{file0.correlationOutputFiles.missing_count}}
                  </div>
                  <div v-if="file1 != null">
                    Second File Rows Total: {{file1.fileMetadata.rows}}
                  </div>
                  <div v-if="file1 != null">
                    Second File Rows Used: {{file1.fileMetadata.rows - file1.correlationOutputFiles.missing_count}}
                  </div>
                  <div v-if="file1 != null">
                    Second File Rows Missing Data: {{file1.correlationOutputFiles.missing_countt}}
                  </div>

                </div>

              </div>

            </v-card>

          </v-col>
          <v-col cols="6">
            <div>
              <v-text-field
                label="File 1 Output"
                v-model="file0.fileOutputName"
                suffix=".csv"
                outlined
                dense
              >
              </v-text-field>
            </div>

            <div>
              <v-text-field
                v-if="file1 != null"
                label="File 2 Output"
                v-model="file1.fileOutputName"
                suffix=".csv"
                outlined
                dense
              >
              </v-text-field>
            </div>
            <div class="overline">Additional File Outputs</div>
            <div>
              <v-switch
                label="Export rows with missing data in seperate file (row indexes included)."
                v-model="exportSettings.exportMissingRows"


              ></v-switch>
            </div>
            <div class="text-right">
              <v-btn
                v-if="!loadingFileData"
                color="primary"
                rounded
                dark
                depressed
                @click="$emit('saveFiles', exportSettings)"


              >
                Save Files
              </v-btn>

            </div>
          </v-col>

        </v-row>
      </v-layout>
    </div>
  </v-card>



</template>

<script>
//packages

//support code


//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepFileOutput',
  components: {
    StepHeading
  },
  props: [
    'stepNumber',
    'stepTitle',
    'loadingFileData',
    'file0',
    'file1',
    'outputList',
  ],
  data() {
    return {
      exportSettings: {
        exportMissingRows: true
      }

    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },
}
</script>
