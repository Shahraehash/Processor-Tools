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
      <p>
        Identify the column containing your target variable to ensure it is maintain in the output.
      </p>
      <v-layout class="ma-5">

        <v-row wrap>
          <v-col cols="6">
            <v-autocomplete
              clearable
              outlined
              label="Target Column"
              v-model="file0.target"
              :items="file0.fileMetadata.column_names_reversed"
              @change="targetColumnChanged"
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-layout>
      <div v-if="file0.target != null" class="body-1">
        <div v-if="targetValid == true" >
          <v-icon color="green" >mdi-check-circle</v-icon> Valid target column.

        </div>
        <div v-if="targetValid == false" >
          <v-icon color="red" >mdi-alert-circle</v-icon> The selected target column is not valid. There must be two unique values.
        </div>
      </div>

    </div>
  </v-card>


</template>

<script>
//packages

//support code


//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'FeatureSelector',
  components: {
    StepHeading
  },
  props: [
    'file0',
    'stepNumber',
    'stepTitle'
  ],
  data() {
    return {
      targetValid: null

    }
  },
  methods: {
    targetColumnChanged(target) {
      this.file0.validateTarget(target).then(response => {
        this.targetValid = true
        console.log(response)
      })

    }
  }
}
</script>
