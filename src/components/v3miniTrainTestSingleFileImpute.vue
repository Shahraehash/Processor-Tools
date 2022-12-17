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
                    <v-radio label="Impute Values (in Training/Initial Test)" 
                        :value="1" 
                        :disabled="!imputeAvailable"
                        ></v-radio>
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

        <v-alert dense color="primary" text v-if="trainingClassSize < 50">We recommend a training class size of at least 50 with an absolute minimum of 25.</v-alert>

        <v3miniPrevalenceBar :combinedFile="combinedFile"/>
        <div class="text-center my-3">
          <v-icon size="50" color="grey" style="transform: rotate(45deg);">mdi-arrow-down-thin</v-icon>
          <span class="grey--text">Allocation</span>
          <v-icon size="50" color="grey" style="transform: rotate(-45deg);">mdi-arrow-down-thin</v-icon>
        </div>
        
        <div class="overline">Training/Initial Testing and Generilization Testing Files</div>        
        <v3miniTrainTestBarMinWidth :graphCounts="graphCounts"/>  
    </div>
  
  </template>
  <script>
import v3miniPrevalenceBar from '@/components/v3miniPrevalenceBar'
import v3miniTrainTestBarMinWidth from '@/components/v3miniTrainTestBarMinWidth.vue'

export default {
    name: 'v3miniTrainTestSingleFileImpute',
    components: {
        v3miniPrevalenceBar,
        v3miniTrainTestBarMinWidth
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
        imputeAvailable() {
            return this.combinedFile.describe.nan.counts[0] > 0 || this.combinedFile.describe.nan.counts[1] > 0
        },
        maxTraining() {
            return this.combinedFile.describe.non_nan.counts[this.combinedFile.describe.minor] - 25
        },        

        graphCounts() {
            if (this.combinedFile) {
                let totalDenominator =  this.combinedFile.describe.total.counts.total

                let trainclassSize = this.trainingClassSize

                let missingZero = this.combinedFile.describe.nan.counts[0]
                let missingOne = this.combinedFile.describe.nan.counts[1] 
             


                let total = {
                    train: {
                        0: 0,
                        1: 0
                    },
                    test: {
                        0: 0,
                        1: 0
                    },
                    remainder: {
                        0: 0,
                        1: 0
                    }
                }

                let missing = {
                    train: {
                        0: 0,
                        1: 0
                    },
                    test: {
                        0: 0,
                        1: 0
                    }
                }

                let imputed = {
                    train: {
                        0: 0,
                        1: 0
                    },
                    test: {
                        0: 0,
                        1: 0
                    }
                }

                total['train'] = {
                    0: trainclassSize,
                    1: trainclassSize
                }

                //Removing missing values
                if (this.missingValuesOption == 0) {
                    imputed['train'] = {
                        0: 0,
                        1: 0,
                    }
                    total['remainder'][0] += missingZero
                    total['remainder'][1] += missingOne                    
                }

                //Imputing missing values
                else if (this.missingValuesOption == 1) {

                    //Method to make sure we don't impute more than the class size
                    let imputationReminderSize = ((classSize, missingCounts) => {
                        if (classSize >= missingCounts) {
                            return {imputed: missingCounts, remainder: 0}
                        }
                        else {
                            return {imputed: trainclassSize, remainder: missingCounts - classSize}
                        }
                    })
                    
                    imputed['train'] = {
                        0: imputationReminderSize(trainclassSize, missingZero).imputed,
                        1: imputationReminderSize(trainclassSize, missingOne).imputed,
                    }
                    total['remainder'][0] += imputationReminderSize(trainclassSize, missingZero).remainder
                    total['remainder'][1] += imputationReminderSize(trainclassSize, missingOne).remainder                 
                }

                
                let testZero = this.combinedFile.describe['non_nan'].counts[0] - (this.trainingClassSize - imputed.train[0])
                let testOne = this.combinedFile.describe['non_nan'].counts[1] - (this.trainingClassSize - imputed.train[1])


                total['test'] = {
                    0: testZero,
                    1: testOne
                }

                //calculate original prevalence
                if (this.prevalenceOption == 1) {
                    let calcTotal = testZero + testOne
                    let prevelenceCurrentClassZero = testZero / calcTotal
                    let prevelenceOriginalClassZero = this.combinedFile.describe.total.percent[0] / 100

                    if (prevelenceCurrentClassZero > prevelenceOriginalClassZero) {
                        let newTotal = Math.round(testOne /  (1 - prevelenceOriginalClassZero))
                        let newClassZero = newTotal - testOne
                        total['remainder'][0] += (testZero - newClassZero)
                        total['test'][0] = newClassZero
                       

                    }
                    else {
                        let newTotal = Math.round(testZero / prevelenceOriginalClassZero)
                        let newClassOne = newTotal - testZero
                        total['remainder'][1] += (testOne - newClassOne)
                        total['test'][1] = newClassOne                        

                    }   

                }
          
                return {totalDenominator,total,missing,imputed}
            }        

            else {
                return null
            }

        },


            

    },
    created() {


        
    },
    mounted() {
        this.trainingClassSize = this.combinedFile.segments.train.counts[0]
        this.change()

    },



    methods: {
        change() {
            this.$emit('effect', {
                finalValues: this.graphCounts,
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

  