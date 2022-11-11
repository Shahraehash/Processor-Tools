<template>
    <div>
        <v3miniPrevalenceBar :combinedFile="combinedFile"/>

        <!-- File Settings -->
        <v-row class="mt-5">
            <v-col cols="66">
                <div class="overline">Handle Missing Values</div>
                <v-radio-group
                    @change="change"
                    v-model="missingValuesOption"
                    >
                    <v-radio label="Remove missing values" :value="0"></v-radio>
                    <v-radio label="Keep and Impute Values (in Training/Initial Test)" :value="1"></v-radio>
                </v-radio-group>
            </v-col>

            <v-col cols="6">
                <div class="overline">Handle Prevlence in Generalization Set</div>
                <v-radio-group
                    @change="change"
                    v-model="prevalenceOption"
                    
                    >
                    <v-radio label="Use All Available Data" :value="0"></v-radio>
                    <v-radio label="Maintain Original Data Prevelence" :value="1"></v-radio>
                </v-radio-group>
            </v-col>                
            <v-col cols="12">
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
        </v-row>

      <div class="overline">Allocation of Data</div>        


 
        {{graphObject}}

        
     

        <!-- <v3miniTrainTestBar :graphObject="graphObject"/>   -->
    </div>
  
  </template>
  <script>
import v3miniPrevalenceBar from '@/components/v3miniPrevalenceBar'

//   import v3miniTrainTestBar from '@/components/v3miniTrainTestBar.vue'

export default {
    name: 'v3miniTrainTestSingleFileImpute',
    components: {
    v3miniPrevalenceBar,
    //   v3miniTrainTestBar
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
                toPercent

                let train = {
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
                }
                
                if (this.missingValueOptions == 1) {
                    train['missingCounts'] = {
                            0: this.combinedFile.describe.nan.counts[0],
                            1: this.combinedFile.describe.nan.counts[1],
                        }
                    train['missingPercent'] = {
                            0: toPercent(this.combinedFile.describe.nan.counts[0], this.trainingClassSize),
                            1: toPercent(this.combinedFile.describe.nan.counts[1], this.trainingClassSize),                        

                        }
               
                }

                //Generalization


                // let missingValueMode = this.missingValueOption == 0 ? 'non_nan' : 'total'


                // let test = {
                //     counts: {
                //         0: this.combinedFile.describe[missingValueMode].counts[0] - this.trainingClassSize,
                //         1: this.combinedFile.describe.counts[1] - this.trainingClassSize,
                //     },
                //     percent: {
                //         0: toPercent(this.combinedFile.describe[missingValueMode].counts[0] - this.trainingClassSize, total),
                //         1: toPercent(this.combinedFile.describe[missingValueMode].counts[1] - this.trainingClassSize, total),
                //     },
                //     missingCounts: {
                //         0: 0,
                //         1: 0,
                //     },
                //     missingPercent: {
                //         0: 0,
                //         1: 0,
                //     },
                // }      
                
                
                let remainder = {
                    count: 0,
                    percent: toPercent(0, total)
                }

                return {total, train, remainder}        
        

                

    




            }
            else {
                return null
            }

        },


            

    },
    created() {

        
    },
    mounted() {
        this.trainingClassSize = this.combinedFile.describe.train.counts[0]

    },



    methods: {
        change() {
            this.$emit('effect', {
                describeObj: this.combinedFile.describe,
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

  