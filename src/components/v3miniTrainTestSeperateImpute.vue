<template>
    <div>
        
        <v-row wrap class="mt-3">                    
            <v-col cols="3">
                <div class="overline blue--text">Training/Initial Validation Missing Values</div>
                <v-radio-group
                  v-model="trainMissing"
                  @change="change"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                    <v-radio label="Impute missing values" :value="1" :disabled="!imputeAvailable"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline blue--text">Training/Initial Validation Equalization</div>
                <v-radio-group
                  v-model="trainEqualize"
                  @change="change"
                    >
                    <v-radio :label="trainingIsBalanced ? 'Keep Balanced' : 'Keep Unbalanced'" :value="0"></v-radio>
                    <v-radio :disabled="trainingIsBalanced" label="Downsample Major Class" :value="1"></v-radio>
                    
                </v-radio-group>
            </v-col>  
            <v-col cols="3">
                <div class="overline green--text">Generalization Testing Missing Values</div>
                <v-radio-group
                    color="green"
                    v-model="testMissing"
                    @change="change"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline green--text">Generalization Testing Prevalence</div>
                <v-radio-group
                    color="green"
                    v-model="testPrevalence"
                    @change="change"
                    >
                    <v-radio label="Use all data" :value="0"></v-radio>
                    <v-radio label="Match original file prevelence" :value="1"></v-radio>
                </v-radio-group>
            </v-col>                      
        </v-row>    

        <v3miniTrainTestBarMinWidth :graphCounts="graphCounts"/>  
        <div class="text-center my-3">
          <v-icon size="50" color="grey" >mdi-arrow-down-thin</v-icon>
          <span class="grey--text">Applying File Changes</span>
          <v-icon size="50" color="grey" >mdi-arrow-down-thin</v-icon>
        </div>

        <v3miniTrainTestBarMinWidth :graphCounts="graphCountsWithChanges"/>   
    </div>


  
  </template>
  <script>

  import v3miniTrainTestBarMinWidth from '@/components/v3miniTrainTestBarMinWidth.vue'

  export default {
    name: 'v3miniTrainTestSeperateImpute',
    components: {

      v3miniTrainTestBarMinWidth
    },
    props: 
      {
        train: {
          type: Object,
          required: true
        },
        test: {
          type: Object,
          required: true
        },   
              
    },
    watch: {

    },
    data() {
      return {
        trainMissing: 0,
        trainEqualize: 0,
        testMissing: 0,
        testPrevalence: 0
      }

    },
    computed: {
      uniqueClasses() {
        if (this.train && this.test) {
          // Get unique classes from both train and test files
          const trainClasses = this.train.describe.unique_classes || Object.keys(this.train.describe.total.counts).filter(key => key !== 'total').map(Number);
          const testClasses = this.test.describe.unique_classes || Object.keys(this.test.describe.total.counts).filter(key => key !== 'total').map(Number);
          
          // Combine and deduplicate classes
          const allClasses = [...new Set([...trainClasses, ...testClasses])].sort((a, b) => a - b);
          return allClasses;
        }
        return [0, 1]; // fallback to binary
      },
      
      isMultiClass() {
        return this.uniqueClasses.length > 2;
      },

      imputeAvailable() {
        return this.uniqueClasses.some(cls => 
          (this.train.describe.nan.counts[cls] || 0) > 0 || 
          (this.test.describe.nan.counts[cls] || 0) > 0
        );
      },      
      
      trainingIsBalanced(){
        if (this.graphCountsWithChanges && this.trainEqualize != 1) {
          // Check if all classes have equal counts
          const trainCounts = Object.values(this.graphCountsWithChanges.total.train);
          const firstCount = trainCounts[0];
          return trainCounts.every(count => count === firstCount);
        }
        else {
          return false
        }
      },
      graphCounts() {
        if (this.train && this.test) {
          let totalDenominator = this.train.describe.total.counts.total + this.test.describe.total.counts.total

          let total = {
            train: {},
            test: {},
            remainder: this.isMultiClass ? 0 : {}
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
          this.uniqueClasses.forEach(cls => {
            total.train[cls] = this.train.describe.total.counts[cls] || 0;
            total.test[cls] = this.test.describe.total.counts[cls] || 0;
            if (!this.isMultiClass) {
              total.remainder[cls] = 0;
            }
            missing.train[cls] = this.train.describe.nan.counts[cls] || 0;
            missing.test[cls] = this.test.describe.nan.counts[cls] || 0;
            imputed.train[cls] = 0;
            imputed.test[cls] = 0;
          });

          return {totalDenominator, total, missing, imputed, uniqueClasses: this.uniqueClasses, isMultiClass: this.isMultiClass}
        }
        else {
          return null
        }
      },
      graphCountsWithChanges() {
        if (this.graphCounts) {
          let totalDenominator = this.train.describe.total.counts.total + this.test.describe.total.counts.total
          let totalRemainder = 0;

          let total = {
            train: {},
            test: {},
            remainder: this.isMultiClass ? 0 : {}
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
          this.uniqueClasses.forEach(cls => {
            total.train[cls] = 0;
            total.test[cls] = 0;
            if (!this.isMultiClass) {
              total.remainder[cls] = 0;
            }
            missing.train[cls] = 0;
            missing.test[cls] = 0;
            imputed.train[cls] = 0;
            imputed.test[cls] = 0;
          });

          // Training Impute Vs. Drop
          if (this.trainMissing == 0) {
            // Remove missing values
            this.uniqueClasses.forEach(cls => {
              total.train[cls] = this.train.describe.non_nan.counts[cls] || 0;
              const missingCount = this.train.describe.nan.counts[cls] || 0;
              totalRemainder += missingCount;
              if (!this.isMultiClass) {
                total.remainder[cls] += missingCount;
              }
            });
          }
          else if (this.trainMissing == 1) {
            // Impute missing values
            this.uniqueClasses.forEach(cls => {
              total.train[cls] = this.train.describe.total.counts[cls] || 0;
              imputed.train[cls] = this.train.describe.nan.counts[cls] || 0;
            });
          }

          // Training Class Equalization
          if (this.trainEqualize == 1) {
            // Find the minimum class count to downsample all classes to
            const trainCounts = this.uniqueClasses.map(cls => total.train[cls]);
            const minCount = Math.min(...trainCounts);
            
            // Downsample all classes to the minimum count
            this.uniqueClasses.forEach(cls => {
              const excess = total.train[cls] - minCount;
              if (excess > 0) {
                total.train[cls] = minCount;
                totalRemainder += excess;
                if (!this.isMultiClass) {
                  total.remainder[cls] += excess;
                }
              }
            });
          }

          // Testing Data - always remove missing values
          this.uniqueClasses.forEach(cls => {
            total.test[cls] = this.test.describe.non_nan.counts[cls] || 0;
            const missingCount = this.test.describe.nan.counts[cls] || 0;
            totalRemainder += missingCount;
            if (!this.isMultiClass) {
              total.remainder[cls] += missingCount;
            }
          });

          // Test Prevalence Matching
          if (this.testPrevalence == 1) {
            console.log('DEBUG: Prevalence matching activated');
            
            // Calculate original prevalence percentages for each class
            const totalOriginal = this.test.describe.total.counts.total;
            const originalPrevalences = {};
            
            this.uniqueClasses.forEach(cls => {
              originalPrevalences[cls] = (this.test.describe.total.counts[cls] || 0) / totalOriginal;
            });
            
            console.log('DEBUG: Original prevalences:', originalPrevalences);
            console.log('DEBUG: Available test data before prevalence:', {...total.test});
            
            // Calculate total available test data
            const totalAvailable = this.uniqueClasses.reduce((sum, cls) => sum + total.test[cls], 0);
            
            // Find the constraining class - the one that would require the smallest total to maintain its proportion
            let constrainingTotal = Infinity;
            let constrainingClass = null;
            
            this.uniqueClasses.forEach(cls => {
              if (originalPrevalences[cls] > 0 && total.test[cls] > 0) {
                const requiredTotal = Math.floor(total.test[cls] / originalPrevalences[cls]);
                if (requiredTotal < constrainingTotal) {
                  constrainingTotal = requiredTotal;
                  constrainingClass = cls;
                }
              }
            });
            
            console.log('DEBUG: Constraining class:', constrainingClass, 'requires total:', constrainingTotal);
            console.log('DEBUG: Total available before constraint:', totalAvailable);
            
            // Only apply prevalence matching if it would actually reduce the data
            if (constrainingTotal < totalAvailable && constrainingTotal > 0) {
              this.uniqueClasses.forEach(cls => {
                const targetCount = Math.floor(constrainingTotal * originalPrevalences[cls]);
                const excess = total.test[cls] - targetCount;
                
                console.log(`DEBUG: Class ${cls}: ${total.test[cls]} -> ${targetCount} (excess: ${excess})`);
                
                total.test[cls] = Math.max(0, targetCount);
                
                // Add excess to remainder
                if (excess > 0) {
                  totalRemainder += excess;
                  if (!this.isMultiClass) {
                    total.remainder[cls] += excess;
                  }
                }
              });
              
              console.log('DEBUG: Final test data after prevalence:', {...total.test});
              console.log('DEBUG: Total remainder added:', totalRemainder);
            } else {
              console.log('DEBUG: No prevalence adjustment needed - constraint would not reduce data');
            }
          }

          // Set remainder for multi-class
          if (this.isMultiClass) {
            total.remainder = totalRemainder;
          }

          return {totalDenominator, total, missing, imputed, uniqueClasses: this.uniqueClasses, isMultiClass: this.isMultiClass}
        }
        else {
          return null
        }
      }

    },
    created() {
      //when initiall loaded, metadata set by parent, then effect function will updated with watcher
      this.localMetadata = this.metadata
    },
    mounted() {
      this.change()

    },

  
  
    methods: {
      change() {
        this.$emit('effect', {
            finalValues: this.graphCountsWithChanges,
            trainMissing: this.trainMissing,
            trainEqualize: this.trainEqualize,
            testMissing: this.testMissing,
            testPrevalence: this.testPrevalence
        })
      }
    
  
    }
  
  }
  </script>
  <style scoped>



  </style>
