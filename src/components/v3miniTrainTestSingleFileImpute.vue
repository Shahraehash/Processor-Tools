<template>
    <div>
        

        <!-- File Settings -->
        <v-row class="mt-5">
            <v-col cols="4">
                <div class="overline">Set size of training data</div>
                <v-slider
                    style="display: inline-flex; width: 200px"
                    v-model="trainingClassSize"
                    @change="change"
                    :max="maxTraining"
                    :min="25"
                    :step="1"
                    :ticks="true"
                    :thumb-label="true"
                    thumb-color="primary"
                    track-color="primary"
                    tick-size="4"
                    >
                </v-slider>          
            </v-col>               
            <v-col cols="4">
                <div class="overline">Handle Missing Values</div>
                <v-radio-group
                    @change="change"
                    v-model="missingValuesOption"
                    >
                    <v-radio label="Remove missing values" :value="0"></v-radio>
                    <v-radio label="Keep and Impute Values (in Training/Initial Test)" :value="1"></v-radio>
                </v-radio-group>
            </v-col>

            <v-col cols="4">
                <div class="overline">Handle Prevlence in Generalization Set</div>
                <v-radio-group
                    @change="change"
                    v-model="prevalenceOption"
                    
                    >
                    <v-radio label="Use All Available Data" :value="0"></v-radio>
                    <v-radio label="Maintain Original Data Prevelence" :value="1"></v-radio>
                </v-radio-group>
            </v-col>                
     
        </v-row>

        <v3miniPrevalenceBar :combinedFile="combinedFile"/>
        <div class="text-center my-3">
          <v-icon size="75" color="grey">mdi-arrow-down-bold-outline</v-icon>
          <span class="overline grey--text">Allocation</span>
          <v-icon size="75" color="grey">mdi-arrow-down-bold-outline</v-icon>
        </div>
        
        <div class="overline">Training/Initial Testing and Generilization Testing Files</div>        
        <v3miniTrainTestBar :graphObject="graphObject"/>  
    </div>
  
  </template>
  <script>
import v3miniPrevalenceBar from '@/components/v3miniPrevalenceBar'
import v3miniTrainTestBar from '@/components/v3miniTrainTestBar.vue'

export default {
    name: 'v3miniTrainTestSingleFileImpute',
    components: {
        v3miniPrevalenceBar,
        v3miniTrainTestBar
    },
    props: 
        {
        combinedFile: {
            type: Object,
            required: true
        },
        effectMetadata: {
            type: Object,
            required: true,
        },
                
    },
    watch: {
        effectMetadata: {
            handler(newVal) {
            this.localEffectMetadata = newVal
            },
            deep: true
        }        

    },
    data() {
        return {
            missingValuesOption: 0,
            prevalenceOption: 0,  
            trainingClassSize: null,         

        }

    },
    computed: {
        maxTraining() {
            return this.combinedFile.describe.non_nan.counts[this.combinedFile.describe.minor] - 25
        },        

        graphObject() {
            if (this.combinedFile) {
                let total =  this.combinedFile.describe.total.counts.total
                let toPercent = (num, denom) => {return Math.round((num / denom) * 1000)/10}
                let remainderCounter = 0
                remainderCounter

                let train = {}

                if (this.missingValuesOption == 0) {
                    train = {
                        counts: {
                                0: this.trainingClassSize,
                                1: this.trainingClassSize,
                            },
                            percent: {
                                0: toPercent(this.trainingClassSize, total),
                                1: toPercent(this.trainingClassSize, total),
                            },
                            missingCounts: {
                                0: 0,
                                1: 0,
                            },
                            missingPercent: {
                                0: 0,
                                1: 0,
                            },
                            imputedCounts: {
                                0: 0,
                                1: 0,
                            },
                            imputedPercent: {
                                0: 0,
                                1: 0,  
                            },                            
                    }
                    remainderCounter += this.combinedFile.describe.nan.counts.total
               
                }
                
                else if (this.missingValuesOption == 1) {

                    train = {
                        counts: {
                                0: this.trainingClassSize,
                                1: this.trainingClassSize,
                            },
                            percent: {
                                0: toPercent(this.trainingClassSize, total),
                                1: toPercent(this.trainingClassSize, total),
                            },
                            missingCounts: {
                                0: 0,
                                1: 0,
                            },
                            missingPercent: {
                                0: 0,
                                1: 0,  
                            },
                            imputedCounts: {
                                0: this.combinedFile.describe.nan.counts[0],
                                1: this.combinedFile.describe.nan.counts[1],
                            },
                            imputedPercent: {
                                0: toPercent(this.combinedFile.describe.nan.counts[0], this.trainingClassSize),
                                1: toPercent(this.combinedFile.describe.nan.counts[1], this.trainingClassSize),  
                            },
                    }                        
               
                }

                console.log(train)

                //Generalization


                


                let missingValueMode = this.missingValuesOption == 0 ? 'non_nan' : 'total'
                let test = {
                        counts: {
                            0: this.combinedFile.describe[missingValueMode].counts[0] - this.trainingClassSize,
                            1: this.combinedFile.describe[missingValueMode].counts[1] - this.trainingClassSize,
                        },
                        percent: {
                            0: toPercent(this.combinedFile.describe[missingValueMode].counts[0] - this.trainingClassSize, total),
                            1: toPercent(this.combinedFile.describe[missingValueMode].counts[1] - this.trainingClassSize, total),
                        },
                        missingCounts: {
                            0: 0,
                            1: 0,
                        },
                        missingPercent: {
                            0: 0,
                            1: 0,
                        },
                    }   

                //calculate original prevalence
                if (this.prevalenceOption == 1) {
                    let calcTotal = test.counts[0] + test.counts[1]
                    let prevelenceCurrentClassZero = test.counts[0] / calcTotal
                    let prevelenceOriginalClassZero = this.combinedFile.describe.total.percent[0] / 100

                    console.log(prevelenceCurrentClassZero)
                    console.log(prevelenceOriginalClassZero)

                    if (prevelenceCurrentClassZero > prevelenceOriginalClassZero) {
                        let newClassZero = Math.round(prevelenceOriginalClassZero * calcTotal)
                        remainderCounter += (test.counts[0] - newClassZero)
                        test.counts[0] = newClassZero
                        test.percent[0] = toPercent(newClassZero, total)
                        

                    }
                    else {
                        let newClassOne = Math.round((1 - prevelenceOriginalClassZero) * calcTotal)
                        remainderCounter += (test.counts[1] - newClassOne)
                        test.counts[1] = newClassOne
                        test.percent[1] = toPercent(newClassOne, total)
                    }   

                }
                console.log(test)

   
                
                
                let remainder = {
                    count: remainderCounter,
                    percent: toPercent(remainderCounter, total)
                }

                return {total, train, test, remainder}        
        

                

    




            }
            else {
                return null
            }

        },


            

    },
    created() {

        
    },
    mounted() {
        this.trainingClassSize = this.combinedFile.describe.combinedFile.counts[0]

    },



    methods: {
        change() {
            this.$emit('effect', {
                finalValues: this.graphObject,
                missingValuesOption: this.missingValuesOption,
                prevalenceOption: this.prevalenceOption, 
                trainingClassSize: this.trainingClassSize            

            })
        }


    }

    }
  </script>
  <style scoped>



  </style>

  