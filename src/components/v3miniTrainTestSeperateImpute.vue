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
                    <v-radio label="Impute missing values" :value="1"></v-radio>
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
                <div class="overline purple--text">Testing Missing Values</div>
                <v-radio-group
                    color="purple"
                    v-model="testMissing"
                    @change="change"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline purple--text">Testing Prevalence</div>
                <v-radio-group
                    color="purple"
                    v-model="testPrevalence"
                    @change="change"
                    >
                    <v-radio label="Use all data" :value="0"></v-radio>
                    <v-radio label="Match original file prevelence" :value="1"></v-radio>
                </v-radio-group>
            </v-col>                      
        </v-row>    

        <v3miniTrainTestBar :graphObject="graphObject"/>  
        <div class="text-center">
          <v-icon size="75">mdi-arrow-down</v-icon>Applying File Changes <v-icon size="75">mdi-arrow-down</v-icon>
        </div>

        <v3miniTrainTestBar :graphObject="graphObjectWithChanges"/>   
    </div>
  
  </template>
  <script>
  import v3miniTrainTestBar from '@/components/v3miniTrainTestBar.vue'

  export default {
    name: 'v3miniTrainTestSeperateImpute',
    components: {
      v3miniTrainTestBar
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
      trainingIsBalanced(){
        if (this.graphObjectWithChanges) {
          return this.graphObjectWithChanges.train.counts[0] == this.graphObjectWithChanges.train.counts[1] && this.trainEqualize != 1
        }
        else {
          return true
        }
        
      },      
      graphObject() {
        if (this.train && this.test) {
          let total =  this.train.describe.total.counts.total + this.test.describe.total.counts.total
          let toPercent = (num, denom) => {return Math.round((num / denom) * 1000)/10}

          let makeObject = (name) => {
            return {
              counts: {
              0: this[name].describe.total.counts[0],
              1: this[name].describe.total.counts[1],
              },
              percent: {
                0: toPercent(this[name].describe.total.counts[0], total),
                1: toPercent(this[name].describe.total.counts[1], total),
              },
              missingCounts: {
                0: this[name].describe.nan.counts[0],
                1: this[name].describe.nan.counts[1],
              },
              missingPercent: {
                0: this[name].describe.nan.percent[0],
                1: this[name].describe.nan.percent[1],
              },
            }
          }
          let remainder = {
            count: 0,
            percent: 0
          }
          let train = makeObject('train')
          let test = makeObject('test')
          return {total, train, test, remainder}
        }
        else {
          return null
        }

      },
      graphObjectWithChanges() {

        if (this.graphObject) {
          let total =  this.train.describe.total.counts.total + this.test.describe.total.counts.total
          let toPercent = (num, denom) => {return Math.round((num / denom) * 10000)/100}

          //Training
          let remainderCounter = 0

          let train = {}
          console.log(this.train.describe)

          //Training remove missing values
          if (this.trainMissing == 0) {
            train = {
              counts: {
                0: this.train.describe.non_nan.counts[0],
                1: this.train.describe.non_nan.counts[1],
              },
              percent: {
                0: toPercent(this.train.describe.non_nan.counts[0], total),
                1: toPercent(this.train.describe.non_nan.counts[1], total),
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
          //count dropped values

          
        }

        //Training impute missing values    
        else if (this.trainMissing == 1) {
          train = {
              counts: {
                0: this.train.describe.total.counts[0],
                1: this.train.describe.total.counts[1],
              },
              percent: {
                0: toPercent(this.train.describe.total.counts[0], total),
                1: toPercent(this.train.describe.total.counts[1], total),
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
        }

        //Training equalize - down sample majority class
        console.log(this.train)
        if (this.trainEqualize == 1) {
          train['counts'][this.train.describe.major] = train['counts'][this.train.describe.minor]
          train['percent'][this.train.describe.major] = train['percent'][this.train.describe.minor]
          //count dropped values
          remainderCounter += ( train['percent'][this.train.describe.major] - train['percent'][this.train.describe.minor] )

        }

        let trainChange = this.train.describe.total.counts.total - train.counts[0] - train.counts[1]
        remainderCounter += trainChange



        //Testing Data
        let test = {
          counts: {
          0: this.test.describe.non_nan.counts[0],
          1: this.test.describe.non_nan.counts[1],
          },
          percent: {
            0: toPercent(this.test.describe.non_nan.counts[0], total),
            1: toPercent(this.test.describe.non_nan.counts[1], total),
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


        if (this.testPrevalence == 1) { 

          let calcTotal = test.counts[0] + test.counts[1]
          let prevelenceCurrentClassZero = test.counts[0] / calcTotal
          let prevelenceOriginalClassZero = this.test.describe.total.percent[0] / 100

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


          
          console.log(test.percent[0] > this.test.describe.total.percent[0])
          

        }


        //count missing
        remainderCounter += this.test.describe.nan.counts[0] + this.test.describe.nan.counts[1]

          let remainder = {
            count: remainderCounter,
            percent: toPercent(remainderCounter, total)
          }

          return {total, train, test, remainder}          

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

    },

  
  
    methods: {
      change() {
        this.$emit('effect', {
            finalValues: this.graphObjectWithChanges,
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

  