<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    /> 
    <v-card flat outlined class="pa-3 my-2" v-for="(file, index) in filePipeline.files" :key="index">
      <v-row dense >
        <v-col cols="6">
          <v-icon>mdi-target</v-icon>
          {{ file.name }}
        </v-col>
        <v-col cols="6">
          <div>
            {{file.targetValidation.valuesCount}} target value<span v-if="file.targetValidation.valuesCount > 1">s</span>
          </div>
          <div class="my-2">
            <v-chip 
                v-for="(val, i) in file.targetValidation.targetValues"
                :key="i"
                small
                >
                {{val}}
            </v-chip>            
          </div>
          <div>
              <span v-if="file.targetValidation.validTarget == 0">
                  <v-icon color="red" >mdi-alert-circle</v-icon>
                  <span v-if="file.targetValidation.valuesCount > 2">Target column has more than two values.</span>
                  <span v-if="file.targetValidation.valuesCount < 2">Target column has only one value.</span>
              </span>
              <span v-else>
                  <v-icon color="green" >mdi-check-circle</v-icon> Target column is valid
              </span>
           
          </div>

        </v-col>
      </v-row>
    </v-card>


    <div v-if="allTargetListsMatch.fileCount > 1">
        <div class="overline purple--text">Cross-file Validation</div>
        
        <!-- All files have valid targets -->
        <div>
            <div v-if="!allTargetListsMatch.allFilesValid">
                <v-icon color="red" >mdi-alert-circle</v-icon>
                Not all files have valid targets.
            </div>
            <div v-else>
                <v-icon color="green" >mdi-check-circle</v-icon>
                All files have valid targets.
            </div>               
        </div>
        <!-- Targets match between files -->
        <div>
            <div v-if="!allTargetListsMatch.allArraysMatch">
                <v-icon color="red" >mdi-alert-circle</v-icon>
                Targets do not match between files.
            </div>
            <div v-else>
                <v-icon color="green" >mdi-check-circle</v-icon>
                Targets match between files.
            </div>               
        </div>        
    </div>
    <!-- Value Map -->
    <div v-if="allTargetListsMatch.allValid" class="mt-5">
        <div class="overline purple--text">Column Encoding</div>
        Values are automatically mapped to a binary representation. Customize here.
        <v-row class="mt-2 mx-1">
            <v-col cols="3" v-for="(val, cat) in allTargetListsMatch.valueMap" :key="cat">
            <div >
                <v-select outlined dense 
                    :label="cat" 
                    v-model="allTargetListsMatch.valueMap[cat]"
                    :items=[0,1]
                    @change="flipValues($event, cat)"

                    ></v-select>
            </div>            
            </v-col>
        </v-row>        
    </div>
    <div class="text-right" v-if="allTargetListsMatch.allValid">
      <v-btn
        @click="$emit('nextStep', allTargetListsMatch.valueMap)"
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
import _ from 'underscore'

//support code

//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepTargetCheck',
  components: {
    StepHeading,

  },
  data() {
    return {
        allTargetListsMatch: null,
    }
  },
  props: [
    'filePipeline',
    'stepNumber',
    'stepTitle',
    'disableNext',
  ],
  watch: {

  },
  created() {
      this.allTargetListsMatch = this.targetListMatching()
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },  
  computed: {
      
  },
  methods: {
    targetListMatching() {
    let files = this.filePipeline.files

    let values = []
    let validSum = 0
    let valueMap = {}
    files.forEach(file => {
        values.push(file.targetValidation.targetValues)
        validSum += file.targetValidation.validTarget
    })
    values = _.flatten(values)
    values = _.uniq(values)
    values.forEach((value,i) => {
        valueMap[value] = i
    })

    return {
        fileCount: files.length,
        allFilesValid: validSum == files.length,
        allArraysMatch: values.length == 2,
        valueMap,
        allValid: validSum == files.length && values.length == 2
        }
    },
    flipValues(val, cat) {
      //state reset
      let map = this.allTargetListsMatch.valueMap
      for (let i in map) {
        if (i == cat) {
          map[i] = val
        }
        else {
          map[i] = Math.abs(val - 1)
        }
      }
      this.$emit('changeStep')
    },           
  }
}
</script>
