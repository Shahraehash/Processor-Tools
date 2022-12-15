<template>
    <div>
        
        <v-row wrap class="mt-3">                    
            <v-col cols="3">
                <div class="overline blue--text">Training Missing Values</div>
                <v-radio-group
                  v-model="trainMissing"
                  @change="change"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                    <v-radio label="Impute missing values" :value="1" :disabled="!imputeAvailable"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline blue--text">Training Equalization</div>
                <v-radio-group
                  v-model="trainEqualize"
                  @change="change"
                    >
                    <v-radio :label="trainingIsBalanced ? 'Keep Balanced' : 'Keep Unbalanced'" :value="0"></v-radio>
                    <v-radio :disabled="trainingIsBalanced" label="Downsample Major Class" :value="1"></v-radio>
                    
                </v-radio-group>
            </v-col>  
            <v-col cols="3">
                <div class="overline green--text">Testing Missing Values</div>
                <v-radio-group
                    color="green"
                    v-model="testMissing"
                    @change="change"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline green--text">Testing Prevalence</div>
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

      imputeAvailable() {
            return this.train.describe.nan.counts[0] > 0 || this.train.describe.nan.counts[1] > 0
        },      
      trainingIsBalanced(){
        if (this.graphCountsWithChanges) {
          return this.graphCountsWithChanges.total.train[0] == this.graphCountsWithChanges.total.train[1] && this.trainEqualize != 1
        }
        else {
          return true
        }
        
      },      
      graphCounts() {
        if (this.train && this.test) {
          let totalDenominator =  this.train.describe.total.counts.total + this.test.describe.total.counts.total



          let total = {
                    train: {
                        0: this['train'].describe.total.counts[0],
                        1: this['train'].describe.total.counts[1]
                    },
                    test: {
                        0: this['test'].describe.total.counts[0],
                        1: this['test'].describe.total.counts[1]
                    },
                    remainder: {
                        0: 0,
                        1: 0
                    }
                }

          let missing = {
                train: {
                  0: this['train'].describe.nan.counts[0],
                    1: this['train'].describe.nan.counts[1]
                },
                test: {
                    0: this['test'].describe.nan.counts[0],
                    1: this['test'].describe.nan.counts[1]
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


          return {totalDenominator,total,missing,imputed}
        }
        else {
          return null
        }

      },
      graphCountsWithChanges() {

        if (this.graphCounts) {
          let totalDenominator =  this.train.describe.total.counts.total + this.test.describe.total.counts.total



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


          
          //Training Impute Vs. Drop

          if (this.trainMissing == 0) {
            total['train'] = {
              0: this['train'].describe.non_nan.counts[0],
              1: this['train'].describe.non_nan.counts[1]
            }
            total['remainder'][0] += this['train'].describe.nan.counts[0]
            total['remainder'][1] += this['train'].describe.nan.counts[1]

          }
          else if (this.trainMissing == 1) {

            total['train'] = {
              0: this['train'].describe.total.counts[0],
              1: this['train'].describe.total.counts[1]
            }
            imputed['train'] = {
              0: this['train'].describe.nan.counts[0],
              1: this['train'].describe.nan.counts[1]
            }
            
            total['remainder'][0] += 0
            total['remainder'][1] += 0


          }
        
        //Training Class Equalization

        if (this.trainEqualize == 1) {
            let diff = total['train'][this.train.describe.major] - total['train'][this.train.describe.minor]
            total['train'][this.train.describe.major] = total['train'][this.train.describe.minor]
            total['remainder'][this.train.describe.major] += diff
        }          

        // Testing Data

        total['test'] = {
          0: this.test.describe.non_nan.counts[0],
          1: this.test.describe.non_nan.counts[1],          
        }
        total['remainder'][0] += this.test.describe.nan.counts[0]
        total['remainder'][1] += this.test.describe.nan.counts[1]



        if (this.testPrevalence == 1) { 
          let originalClassZeroPrev = this.test.describe.total.percent[0] / 100
          let currentClassZeroPrev = total['test'][0] / ((total['test'][0] + total['test'][1]))
          if (currentClassZeroPrev > originalClassZeroPrev) {
            let newTotal = Math.round(total['test'][1] / (1 - originalClassZeroPrev))
            let newClassZero = newTotal - total['test'][1]
            total['remainder'][0] += (total['test'][0] - newClassZero)
            total['test'][0] = newClassZero
          }
          else {
            let newTotal = Math.round(total['test'][0] / originalClassZeroPrev)
            let newClassOne = newTotal - total['test'][0]
            total['remainder'][1] += (total['test'][1] - newClassOne)
            total['test'][1] = newClassOne
          }
        


        }


        return {totalDenominator,total,missing,imputed}


          







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

  