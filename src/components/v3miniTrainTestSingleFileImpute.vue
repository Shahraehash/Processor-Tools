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
            // For multi-class, check the minimum class size across all classes
            const uniqueClasses = this.combinedFile.describe.unique_classes || [0, 1];
            let minClassSize = Infinity;
            
            uniqueClasses.forEach(cls => {
                const clsKey = String(cls);
                const classSize = this.combinedFile.describe.non_nan.counts[clsKey] || 0;
                if (classSize < minClassSize) {
                    minClassSize = classSize;
                }
            });
            
            return minClassSize < 50;
        },
        maxTrainingSize() {
            // For multi-class, find the minimum class size to determine max training size
            const uniqueClasses = this.combinedFile.describe.unique_classes || [0, 1];
            let minClassSize = Infinity;
            
            uniqueClasses.forEach(cls => {
                const clsKey = String(cls);
                let classSize;
                if (this.missingValuesOption == 0) {
                    classSize = this.combinedFile.describe.non_nan.counts[clsKey] || 0;
                } else if (this.missingValuesOption == 1) {
                    classSize = this.combinedFile.describe.total.counts[clsKey] || 0;
                } else {
                    classSize = 25;
                }
                
                if (classSize < minClassSize) {
                    minClassSize = classSize;
                }
            });
            
            return Math.max(25, minClassSize - 25);
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
            return uniqueClasses.some(cls => {
                const clsKey = String(cls);
                return this.combinedFile.describe.nan.counts[clsKey] > 0;
            });
        },
        maxTraining() {
            // For multi-class, find the minimum class size to determine max training
            const uniqueClasses = this.combinedFile.describe.unique_classes || [0, 1];
            let minClassSize = Infinity;
            
            uniqueClasses.forEach(cls => {
                const clsKey = String(cls);
                const classSize = this.combinedFile.describe.non_nan.counts[clsKey] || 0;
                if (classSize < minClassSize) {
                    minClassSize = classSize;
                }
            });
            
            return Math.max(25, minClassSize - 25);
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
                    remainder: {} // Always use object with class keys for consistency
                }

                let missing = {
                    train: {},
                    test: {}
                }

                let imputed = {
                    train: {},
                    test: {}
                }

                // Initialize data for each class (including remainder) - use consistent string keys
                uniqueClasses.forEach(cls => {
                    const clsKey = String(cls);
                    total.train[clsKey] = trainclassSize;
                    total.test[clsKey] = 0;
                    total.remainder[clsKey] = 0; // Always initialize remainder with class keys
                    missing.train[clsKey] = 0;
                    missing.test[clsKey] = 0;
                    imputed.train[clsKey] = 0;
                    imputed.test[clsKey] = 0;
                });

                //Removing missing values
                if (this.missingValuesOption == 0) {
                    uniqueClasses.forEach(cls => {
                        const clsKey = String(cls);
                        imputed.train[clsKey] = 0;
                        const missingCount = this.combinedFile.describe.nan.counts[clsKey] || 0;
                        total.remainder[clsKey] += missingCount;
                    });
                }

                //Imputing missing values
                else if (this.missingValuesOption == 1) {
                    uniqueClasses.forEach(cls => {
                        const clsKey = String(cls);
                        const missingCount = this.combinedFile.describe.nan.counts[clsKey] || 0;
                        if (trainclassSize >= missingCount) {
                            imputed.train[clsKey] = missingCount;
                        } else {
                            imputed.train[clsKey] = trainclassSize;
                            const remainder = missingCount - trainclassSize;
                            total.remainder[clsKey] += remainder;
                        }
                    });
                }

                // Calculate test allocation for each class
                uniqueClasses.forEach(cls => {
                    const clsKey = String(cls);
                    const nonNanCount = this.combinedFile.describe.non_nan.counts[clsKey] || 0;
                    const testCount = nonNanCount - (trainclassSize - imputed.train[clsKey]);
                    total.test[clsKey] = Math.max(0, testCount);
                    
                    // Add any excess to remainder
                    if (testCount < 0) {
                        total.remainder[clsKey] += Math.abs(testCount);
                    }
                });

                // Apply prevalence adjustment for both binary and multi-class
                if (this.prevalenceOption == 1) {
                    // Calculate original prevalence for each class
                    const totalOriginal = this.combinedFile.describe.total.counts.total;
                    const originalPrevalences = {};
                    
                    uniqueClasses.forEach(cls => {
                        const clsKey = String(cls);
                        originalPrevalences[clsKey] = this.combinedFile.describe.total.counts[clsKey] / totalOriginal;
                    });
                    
                    // Find the limiting factor (class that constrains the total)
                    let limitingFactor = Infinity;
                    uniqueClasses.forEach(cls => {
                        const clsKey = String(cls);
                        if (originalPrevalences[clsKey] > 0 && total.test[clsKey] > 0) {
                            const factor = total.test[clsKey] / originalPrevalences[clsKey];
                            if (factor < limitingFactor) {
                                limitingFactor = factor;
                            }
                        }
                    });
                    
                    // Adjust test allocation for each class based on prevalence
                    if (limitingFactor !== Infinity && limitingFactor > 0) {
                        uniqueClasses.forEach(cls => {
                            const clsKey = String(cls);
                            const targetCount = Math.round(limitingFactor * originalPrevalences[clsKey]);
                            const excess = total.test[clsKey] - targetCount;
                            
                            total.test[clsKey] = Math.max(0, targetCount);
                            
                            // Add excess to remainder (always use class-specific structure)
                            if (excess > 0) {
                                total.remainder[clsKey] += excess;
                            }
                        });
                    }
                }

                
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
