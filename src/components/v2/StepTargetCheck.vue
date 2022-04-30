<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    /> 
    <v-card 
        v-for="(file, index) in filePipeline.metadata.initialFiles" 
        :key="index"
        class="my-2"
        flat
        >
        <div class="overline primary--text">{{file.name}}</div>   
        <div>
            Target Values ({{file.targetValidation.valuesCount}}): 
            <v-chip 
                v-for="(val, i) in file.targetValidation.targetValues"
                :key="i"
                small
                >
                {{val}}
            </v-chip>
        </div>
        <div>
            <div v-if="file.targetValidation.validTarget == 0">
                <v-icon color="red" >mdi-alert-circle</v-icon>
                <span v-if="file.targetValidation.valuesCount > 2">Target column has more than two values.</span>
                <span v-if="file.targetValidation.valuesCount < 2">Target column has only one value.</span>
            </div>
            <div v-else>
                <v-icon color="green" >mdi-check-circle</v-icon> Target column is valid
            </div>
        </div>  
              
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
    StepHeading
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
  ],
  watch: {
    filePipeline: () => {
     this.allTargetListsMatch = this.checkAllTargetListsMatch()

    }
  },
  created() {
      this.allTargetListsMatch = this.targetListMatching()
  },
  computed: {
      
  },
  methods: {
    targetListMatching() {
    let files = this.filePipeline.metadata.initialFiles

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
      let map = this.allTargetListsMatch.valueMap
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
