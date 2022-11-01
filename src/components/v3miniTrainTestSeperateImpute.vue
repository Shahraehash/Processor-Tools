<template>
    <div>
        
        <v-row wrap class="mt-3">                    
            <v-col cols="3">
                <div class="overline blue--text">Training Missing Values</div>
                <v-radio-group
                  v-model="trainMissing"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                    <v-radio label="Impute missing values" :value="1"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline blue--text">Training Equalization</div>
                <v-radio-group
                  v-model="trainEqualize"
                    >
                    <v-radio label="Leave Unbalanced" :value="0"></v-radio>
                    <v-radio :disabled="true" label="Downsample Major Class" :value="1"></v-radio>
                    
                </v-radio-group>
            </v-col>  
            <v-col cols="3">
                <div class="overline purple--text">Testing Missing Values</div>
                <v-radio-group
                    color="purple"
                    v-model="testMissing"
                    >
                    <v-radio label="Remove all missing values" :value="0"></v-radio>
                </v-radio-group>
            </v-col>
            <v-col cols="3">
                <div class="overline purple--text">Testing Prevalence</div>
                <v-radio-group
                    color="purple"
                    v-model="testPrevalence"
                    >
                    <v-radio label="Use all data" :value="0"></v-radio>
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
      graphObject() {
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
      },
      graphObjectWithChanges() {
        let total =  this.train.describe.total.counts.total + this.test.describe.total.counts.total
        let toPercent = (num, denom) => {return Math.round((num / denom) * 1000)/10}

        //Training


        let train = {
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

        let nan = this.train.describe.nan.total + this.test.describe.nan.total

        let remainder = {
          count: nan,
          percent: toPercent(nan, total)
        }

        return {total, train, test, remainder}

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
            describeObj: this.describe,
            missingValuesOption: this.missingValuesOption,
            prevalenceOption: this.prevalenceOption, 
            trainingClassSize: this.localMetadata.train.counts[0]})
      }
    
  
    }
  
  }
  </script>
  <style scoped>



  </style>

  