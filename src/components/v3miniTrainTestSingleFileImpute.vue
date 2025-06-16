<template>
    <div>
        <!-- File Settings -->
        <v-row class="mt-5">
            <v-col cols="4">
                <div class="overline">Size of training/initial validation data</div>
                <v-slider
                    style="display: inline-flex; width: 250px"
                    v-model="trainingClassSize"
                    @change="change"
                    :max="maxTrainingSize"
                    :min="minTrainingSize"
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
                    <v-radio label="Remove missing values" 
                        :value="0"
                        :disabled="onlyAllowImpute"
                        ></v-radio>
                    <v-radio label="Impute Values (in Training/Initial Test)" 
                        :value="1" 
                        :disabled="!imputeAvailable"
                        ></v-radio>
                </v-radio-group>
            </v-col>

            <v-col cols="4">
                <div class="overline">Handle Prevalence in Generalization Set</div>
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
        },
    },
    data() {
        return {
            missingValuesOption: 0,
            prevalenceOption: 0,  
            trainingClassSize: 25,         

        }

    },
    computed: {
        onlyAllowImpute() {
            return this.combinedFile.describe.non_nan.counts[this.combinedFile.describe.minor] < 50
        },
        maxTrainingSize() {
            if (this.missingValuesOption == 0) {
                return this.combinedFile.describe.non_nan.counts[this.combinedFile.describe.minor] - 25
            }
            else if (this.missingValuesOption == 1) {
                return this.combinedFile.describe.total.counts[this.combinedFile.describe.minor] - 25
            }
            else {
                return 25
            }
        },
        minTrainingSize() {
            return 25
        },
        
        meanTrainingSize() {
            return Math.round((this.maxTrainingSize + this.minTrainingSize) / 2)
        },

        imputeAvailable() {
            // Check if any class has missing values (multi-class support)
            const uniqueClasses = this.combinedFile.describe.unique_classes || [0, 1];
            return uniqueClasses.some(cls => this.combinedFile.describe.nan.counts[cls] > 0);
        },
        maxTraining() {
            return this.combinedFile.describe.non_nan.counts[this.combinedFile.describe.minor] - 25
        },

        graphCounts() {
            if (this.combinedFile) {
                let totalDenominator = this.combinedFile.describe.total.counts.total
                let trainclassSize = this.trainingClassSize

                // Get all unique classes dynamically
                const uniqueClasses = this.combinedFile.describe.unique_classes || [0, 1];
                const isMultiClass = uniqueClasses.length > 2;
                
                let total = {
                    train: {},
                    test: {},
                    remainder: isMultiClass ? 0 : {} // For multi-class, remainder is a single number
                }

                let missing = {
                    train: {},
                    test: {}
                }

                let imputed = {
                    train: {},
                    test: {}
                }

                // Initialize data for each class
                uniqueClasses.forEach(cls => {
                    total.train[cls] = trainclassSize;
                    total.test[cls] = 0;
                    if (!isMultiClass) {
                        total.remainder[cls] = 0;
                    }
                    missing.train[cls] = 0;
                    missing.test[cls] = 0;
                    imputed.train[cls] = 0;
                    imputed.test[cls] = 0;
                });

                let totalRemainder = 0;

                //Removing missing values
                if (this.missingValuesOption == 0) {
                    uniqueClasses.forEach(cls => {
                        imputed.train[cls] = 0;
                        const missingCount = this.combinedFile.describe.nan.counts[cls] || 0;
                        totalRemainder += missingCount;
                        if (!isMultiClass) {
                            total.remainder[cls] += missingCount;
                        }
                    });
                }

                //Imputing missing values
                else if (this.missingValuesOption == 1) {
                    uniqueClasses.forEach(cls => {
                        const missingCount = this.combinedFile.describe.nan.counts[cls] || 0;
                        if (trainclassSize >= missingCount) {
                            imputed.train[cls] = missingCount;
                        } else {
                            imputed.train[cls] = trainclassSize;
                            const remainder = missingCount - trainclassSize;
                            totalRemainder += remainder;
                            if (!isMultiClass) {
                                total.remainder[cls] += remainder;
                            }
                        }
                    });
                }

                // Calculate test allocation for each class
                uniqueClasses.forEach(cls => {
                    const nonNanCount = this.combinedFile.describe.non_nan.counts[cls] || 0;
                    const testCount = nonNanCount - (trainclassSize - imputed.train[cls]);
                    total.test[cls] = Math.max(0, testCount);
                    
                    // Add any excess to remainder
                    if (testCount < 0) {
                        totalRemainder += Math.abs(testCount);
                        if (!isMultiClass) {
                            total.remainder[cls] += Math.abs(testCount);
                        }
                    }
                });

                // For prevalence adjustment in multi-class, we'll keep it simple for now
                if (this.prevalenceOption == 1 && !isMultiClass) {
                    // Only apply detailed prevalence adjustment for binary classification
                    let testZero = total.test[0];
                    let testOne = total.test[1];
                    let calcTotal = testZero + testOne;
                    let prevelenceCurrentClassZero = testZero / calcTotal;
                    let prevelenceOriginalClassZero = this.combinedFile.describe.total.percent[0] / 100;

                    if (prevelenceCurrentClassZero > prevelenceOriginalClassZero) {
                        let newTotal = Math.round(testOne / (1 - prevelenceOriginalClassZero));
                        let newClassZero = newTotal - testOne;
                        total.remainder[0] += (testZero - newClassZero);
                        total.test[0] = newClassZero;
                    }
                    else {
                        let newTotal = Math.round(testZero / prevelenceOriginalClassZero);
                        let newClassOne = newTotal - testZero;
                        total.remainder[1] += (testOne - newClassOne);
                        total.test[1] = newClassOne;
                    }
                }

                // Set remainder for multi-class
                if (isMultiClass) {
                    total.remainder = totalRemainder;
                }

                console.log('DEBUG FRONTEND: uniqueClasses:', uniqueClasses);
                console.log('DEBUG FRONTEND: isMultiClass:', isMultiClass);
                console.log('DEBUG FRONTEND: total structure:', total);
                
                return {totalDenominator, total, missing, imputed, uniqueClasses, isMultiClass}
            }        
            else {
                return null
            }
        },


            

    },
    created() {


        
    },
    mounted() {
        console.log('DEBUG: v3miniTrainTestSingleFileImpute mounted');
        console.log('DEBUG: combinedFile:', this.combinedFile);
        console.log('DEBUG: combinedFile.describe:', this.combinedFile?.describe);
        console.log('DEBUG: unique_classes:', this.combinedFile?.describe?.unique_classes);
        
        if (this.onlyAllowImpute) {
            this.missingValuesOption = 1
        }
        this.trainingClassSize = this.maxTrainingSize

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
