<template>
    <div>
        <div v-if="graphPercents">
            

            <!-- GROUP BARS -->
            <div style="width:100%; height: 40px; white-space: nowrap;" >
            
            <!-- Train -->
            <div
                class="group-box data-set-box right-spacer"
                v-bind:style="{
                background: mxBarColors.train,
                width: getTotalPercentForGroup('train') + '%',
                }"
                >
                Train/Initital Validation 
            </div>

            <!-- Test -->
            <div
                class="group-box data-set-box right-spacer"
                v-bind:style="{
                background: mxBarColors.test,
                width: getTotalPercentForGroup('test') + '%',
                }"
                >
                Generalization Test
            </div>      
            
            <!-- Remainder -->
            <div
                class="group-box removed-box-width"
                v-bind:style="{
                background: mxBarColors.blank,
                width: getTotalPercentForGroup('remainder') + '%',
                }"
                >
                Removed
            </div>        
            </div>



            <!-- Class Bars -->
            <div style="width:100%; white-space: nowrap;">     
            
            <!-- Multi-class visualization -->
            <div v-if="graphCounts.isMultiClass">
                <!-- Train bars for each class -->
                <div 
                    v-for="(cls, index) in graphCounts.uniqueClasses" 
                    :key="'train-' + cls"
                    class="group-box class-box class-box-width"
                    :class="{ 'right-spacer': index === graphCounts.uniqueClasses.length - 1 }"
                    v-bind:style="{
                        background: getClassColor(index),
                        width: graphPercents.totalPercent.train[cls] + '%',
                    }"
                >
                    <!-- Missing -->
                    <div class="missing class-box"
                        v-bind:style="{
                        background: mxBarColors.missing,
                        width: graphPercents.missingPercent.train[cls] +'%'
                        }"
                    ></div>

                    <!-- Imputed -->
                    <div class="imputed class-box"
                        v-bind:style="{
                        width: graphPercents.imputedPercent.train[cls] + '%'
                        }"
                    ></div>       
                    
                    c{{cls}}: {{graphCounts.total.train[cls]}}
                </div>

                <!-- Test bars for each class -->
                <div 
                    v-for="(cls, index) in graphCounts.uniqueClasses" 
                    :key="'test-' + cls"
                    class="group-box class-box class-box-width"
                    :class="{ 'right-spacer': index === graphCounts.uniqueClasses.length - 1 }"
                    v-bind:style="{
                        background: getClassColor(index),
                        width: graphPercents.totalPercent.test[cls] + '%',
                    }"
                >
                    <!-- Missing -->
                    <div class="missing class-box"
                        v-bind:style="{
                        background: mxBarColors.missing,
                        width: graphPercents.missingPercent.test[cls] +'%'
                        }"
                    ></div>

                    <!-- Imputed -->
                    <div class="imputed class-box"
                        v-bind:style="{
                        width: graphPercents.imputedPercent.test[cls] + '%'
                        }"
                    ></div>   

                    c{{cls}}: {{graphCounts.total.test[cls]}}
                </div>

                <!-- Remainder -->
                <div
                    class="group-box removed-box-width"
                    v-bind:style="{
                    background: mxBarColors.missing,
                    width: graphPercents.totalPercent.remainder + '%'
                    }"
                >
                    {{graphCounts.total.remainder}}
                </div>
            </div>

            <!-- Binary classification visualization (original) -->
            <div v-else>
                <!-- Train Class 0 -->
                <div
                    class="group-box class-box class-box-width"
                    v-bind:style="{
                    background: mxBarColors.classZero,
                    width:  graphPercents.totalPercent.train[0] + '%',
                    }"
                    >

                    <!-- Missing -->
                    <div class="missing class-box"
                        v-bind:style="{
                        background: mxBarColors.missing,
                        width: graphPercents.missingPercent.train[0] +'%'
                        }"
                    ></div>

                    <!-- Imputed -->
                    <div class="imputed class-box"
                        v-bind:style="{
                        width: graphPercents.imputedPercent.train[0] + '%'
                        }"
                    ></div>       
                    
                    c0: {{graphCounts.total.train[0]}}
                </div>

                <!-- Train Class 1 -->
                <div
                    class="group-box class-box class-box-width right-spacer "
                    v-bind:style="{
                    background: mxBarColors.classOne,
                    width:  graphPercents.totalPercent.train[1] + '%',

                    }"
                    >

                    <!-- Missing -->
                    <div class="missing class-box imputed-missing-right"
                        v-bind:style="{
                        background: mxBarColors.missing,
                        width: graphPercents.missingPercent.train[1] +'%'
                        }"
                    ></div>

                    <!-- Imputed -->
                    <div class="imputed class-box imputed-missing-right"
                        v-bind:style="{
                        width: graphPercents.imputedPercent.train[1] + '%'
                        }"
                    ></div>   

                    c1: {{graphCounts.total.train[1]}}
                </div>        
                
                <!-- Test Class 0 -->
                <div
                    class="group-box class-box class-box-width"
                    v-bind:style="{
                    background: mxBarColors.classZero,
                    width:  graphPercents.totalPercent.test[0] +'%',

                    }"
                    >

                    <!-- Missing -->
                    <div class="missing class-box"
                        v-bind:style="{
                        background: mxBarColors.missing,
                        width: graphPercents.missingPercent.test[0] +'%'
                        }"
                    ></div>

                    <!-- Imputed -->
                    <div class="imputed class-box"
                        v-bind:style="{
                        width: graphPercents.imputedPercent.test[0] + '%'
                        }"
                    ></div>   

                    c0: {{graphCounts.total.test[0]}}
                </div>   
                
                <!-- Test Class 1 -->
                <div
                    class="group-box class-box class-box-width right-spacer"
                    v-bind:style="{
                    background: mxBarColors.classOne,
                    width: graphPercents.totalPercent.test[1] + '%',

                    }"
                    >

                    <!-- Missing -->
                    <div class="missing class-box imputed-missing-right"
                        v-bind:style="{
                        background: mxBarColors.missing,
                        width: graphPercents.missingPercent.test[1] +'%'
                        }"
                    ></div>

                    <!-- Imputed -->
                    <div class="imputed class-box imputed-missing-right"
                        v-bind:style="{
                        width: graphPercents.imputedPercent.test[1] + '%'
                        }"
                    ></div>   

                    c1: {{graphCounts.total.test[1]}}
                </div>        
                
                <!-- Remainder -->
                <div
                    class="group-box removed-box-width "
                    v-bind:style="{
                    background: mxBarColors.missing,
                    width: graphPercents.totalPercent.remainder[0] + graphPercents.totalPercent.remainder[1] + '%'
                    }"
                    
                    >

                    {{graphCounts.total.remainder[0] + graphCounts.total.remainder[1]}}
                </div>
            </div>
        </div>
        <div v-if="graphCounts.isMultiClass">
            Showing allocation for all {{graphCounts.uniqueClasses.length}} classes combined ({{graphCounts.uniqueClasses.join(', ')}})
        </div>
        <div v-else>
            c0 = Class 0, c1 = Class 1
        </div>
        </div>
        <v-alert text type="warning" v-if="graphPercents.imputedPercent.train[0] + graphPercents.imputedPercent.train[1] > 30">
            More than 30% of the training data is being imputed. This may cause problems with the model.
        </v-alert>
        <!-- <v-row>
            <v-col cols="6">
                <vue-json-pretty :data="graphCounts"></vue-json-pretty>
            </v-col>
            <v-col cols="6">
                <vue-json-pretty :data="graphPercents"></vue-json-pretty>
            </v-col>            
        </v-row> -->

        
    </div>
  
  </template>
  <script>
  import v3Mixin from '@/components/v3Mixin';
//   import VueJsonPretty from 'vue-json-pretty';
//     import 'vue-json-pretty/lib/styles.css';


  export default {
    name: 'v3miniTrainTestBar',

    mixins: [v3Mixin],
    props: 
      {
        graphCounts: {
          type: Object,
          required: true
        },
          

   
    },
    watch: {

    },
    data() {
      return {
        minBarPercent: 0,

      }

    },
    computed: {
        graphPercents() {
            console.log('DEBUG VIZ: Received graphCounts:', this.graphCounts);
            console.log('DEBUG VIZ: isMultiClass:', this.graphCounts?.isMultiClass);
            console.log('DEBUG VIZ: uniqueClasses:', this.graphCounts?.uniqueClasses);
            let minPercent = 7.5
            let minPercentSum = 0
            let otherPercent = 0

            const toPercent = ((num, denom, type) => {
                console.log('kind', type)
                let percent = Math.round(num / denom * 100)


                //use special logic for remainder -- half other sizes
                if (type == 'remainder') {
                    if (percent < (minPercent / 2) && num > 0) {
                    minPercentSum += (minPercent / 2 )
                    return (minPercent / 2)
                    }
                    else {
                        otherPercent += percent
                        return percent
                    }  
                }
                else {
                    if (percent < minPercent && num > 0) {
                    minPercentSum += minPercent
                    return minPercent
                    }
                    else {
                        otherPercent += percent
                        return percent
                    }                    
                }



            })

            let totalPercent = {}

            let total = this.graphCounts.total
            let missing = this.graphCounts.missing
            let imputed = this.graphCounts.imputed
            let denom = this.graphCounts.totalDenominator

            for (let key in total) {
                let entry = total[key]
                totalPercent[key] = {}
                for (let subkey in entry) {
                    let val = entry[subkey]
                    totalPercent[key][subkey] = toPercent(val, denom, key)

                }
            }

            missing
            imputed

            let missingPercent = {}

            for (let key in missing) {
                let entry = missing[key]
                missingPercent[key] = {}
                for (let subkey in entry) {
                    let val = entry[subkey]
                    missingPercent[key][subkey] = Math.round((val/  total[key][subkey]) * 100)

                }
            }


            let imputedPercent = {}
            imputedPercent
            
            for (let impKey in imputed) {
                let entry = imputed[impKey]
                imputedPercent[impKey] = {}
                for (let impsubkey in entry) {
                    let val = entry[impsubkey]
                    imputedPercent[impKey][impsubkey] = Math.round((val/  total[impKey][impsubkey] ) * 100)


                }
            }


            const scaleRemainingPercent = (percentVal) => {
                let remainingPercent = 100 - (minPercentSum)
                let percentOfOther = percentVal / otherPercent
                let scaledPercent = Math.round(percentOfOther * remainingPercent)

                return scaledPercent
            }

            for (let x in totalPercent) {
                console.log(x)
                let entry = totalPercent[x]
                for (let y in entry) {
                    let val = entry[y]
                    if (val > minPercent) {
                        totalPercent[x][y] = scaleRemainingPercent(val)
                    }
                }
            }            



            return {minPercent, minPercentSum, totalPercent, missingPercent, imputedPercent}



            



            

        }


    },
    created() {

    },
    mounted() {

    },

  
  
    methods: {
        getClassColor(index) {
            // Generate different colors for each class
            const colors = [
                this.mxBarColors.classZero,
                this.mxBarColors.classOne,
                '#FF6B6B', // Red
                '#4ECDC4', // Teal
                '#45B7D1', // Blue
                '#96CEB4', // Green
                '#FFEAA7', // Yellow
                '#DDA0DD', // Plum
                '#98D8C8', // Mint
                '#F7DC6F'  // Light Yellow
            ];
            return colors[index % colors.length];
        },
        
        getTotalPercentForGroup(groupType) {
            if (!this.graphPercents || !this.graphCounts) {
                return 0;
            }
            
            const groupData = this.graphPercents.totalPercent[groupType];
            
            if (this.graphCounts.isMultiClass) {
                // For multi-class, sum all class percentages
                if (groupType === 'remainder') {
                    // Remainder is a single number for multi-class
                    return groupData || 0;
                } else {
                    // Sum percentages for all classes
                    return this.graphCounts.uniqueClasses.reduce((total, cls) => {
                        return total + (groupData[cls] || 0);
                    }, 0);
                }
            } else {
                // For binary classification, use the original logic
                if (groupType === 'remainder') {
                    return (groupData[0] || 0) + (groupData[1] || 0);
                } else {
                    return (groupData[0] || 0) + (groupData[1] || 0);
                }
            }
        }
    }
  
  }
  </script>

    <style scoped>
    .group-box {        
        position: relative;
        transition: width 0.5s;
        display: inline-block;
        text-align: center;
        color: white;
        overflow: hidden;
        padding-top: 8px;
        height:40px;
    }    
    .class-box {
        padding-top: 8px;
        height:40px;
    }

    .right-spacer {
        border-right: 5px white solid;
    }
    .missing {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1;
        padding-top: 8px;
        height:40px;
        opacity: 0.8
        
    }
    .imputed {
        position: absolute;
        top: 0;
        z-index: 1;
        background: orange;
        opacity: 0.4;
    }
    .imputed-missing-right {
        right: 0
    }
    .key-box {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 5px;
        margin-right: 5px;
        margin-left: 15px;
    }

  </style>
