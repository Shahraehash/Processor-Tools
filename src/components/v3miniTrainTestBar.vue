<template>
    <div>
        
            <div style="width:100%">
                    <div
                        class="title-box"
                        v-bind:style="{
                        background: '#2196F3',
                        width:  graph.train.percent[0] + graph.train.percent[1] + '%'
                        }"
                        
                        >
                        Training
                    </div>
                    <div
                        class="title-box"
                        v-bind:style="{
                        background: '#9C27B0',
                        width:  graph.test.percent[0] + graph.test.percent[1] + '%'
                        }"
                        >
                        Generalization Testing
                    </div>        
                    <div
                        class="title-box"
                        v-bind:style="{
                        background: 'white',
                        width: remainder.percent + '%'
                        }"
                        
                        >
                    </div>        
                </div>

                <div style="width:100%">     
                    <div
                        class="title-box "
                        v-bind:style="{
                        background: '#009688',
                        width:  graph.train.percent[0] + '%'
                        }"
                        >
                        


                 
                        {{graph.train.counts[0]}}
                    </div>
                    <div
                        class="title-box "
                        v-bind:style="{
                        background: '#4CAF50',
                        width:  graph.train.percent[1] + '%'
                        }"
                        >
                        {{graph.train.counts[1]}}
                

                    </div>        
                    <div
                        class="title-box"
                        v-bind:style="{
                        background: '#009688',
                        width:  graph.test.percent[0] + '%'
                        }"
                        >
                        {{graph.test.counts[0]}}
                    </div>   
                    <div
                        class="title-box"
                        v-bind:style="{
                        background: '#4CAF50',
                        width: graph.test.percent[1] + '%' 
                        }"
                        >
                        {{graph.test.counts[1]}}
                        
                    </div>        
                    <div
                        class="title-box"
                        v-bind:style="{
                        background: 'grey',
                        width: remainder.percent + '%'
                        }"
                        
                        >
                        {{remainder.counts}}
                    </div>   
                </div>
                            

        
                





  
    </div>
  
  </template>
  <script>


  export default {
    name: 'v3miniTrainTestBar',
    props: 
      {
        test: {
          type: Object,
          required: true
        },
        train: {
          type: Object,
          required: true
        },   
        remainder: {
          type: Object,
          required: false,
          default: () => {
            return {
              counts: 0,
              percent: 0
            }
          }
        },                
    },
    computed: {
        graph() {
            return {
                train: {
                    counts: {
                        0: this.train.describe.total.counts[0],
                        1: this.train.describe.total.counts[1]
                    },
                    percent: {
                        0: this.covertToPercent(this.train.describe.total.counts[0]),
                        1: this.covertToPercent(this.train.describe.total.counts[1])
                    },
                    missing: {
                        0: this.train.describe.nan.counts[0],
                        1: this.train.describe.nan.counts[1]
                    },
                    // percentMissing: {
                    //     0: this.toPercent(this.train.describe.nan.counts[0], this.train.describe.total.counts[0]),
                    //     1: this.toPercent(this.train.describe.nan.counts[1], this.train.describe.total.counts[1])
                    // }
                },
                test: {
                    counts: {
                        0: this.test.describe.total.counts[0],
                        1: this.test.describe.total.counts[1]
                    },
                
                    percent: {
                        0: this.covertToPercent(this.test.describe.total.counts[0]),
                        1: this.covertToPercent(this.test.describe.total.counts[1])
                    },
                    missing: {
                        0: this.test.describe.nan.counts[0],
                        1: this.test.describe.nan.counts[1]
                    },
                    // percentMissing: {
                    //     0: this.toPercent(this.test.describe.nan.counts[0], this.test.describe.total.counts[0]),
                    //     1: this.toPercent(this.test.describe.nan.counts[1], this.test.describe.total.counts[0])
                    // }                    
                }                
            }
        }
        

    },
    data() {
      return {

      }

    },
    methods: {
        covertToPercent(val) {
            let perc = val / (this.train.describe.total.counts.total + this.test.describe.total.counts.total)
            return Math.round(perc * 1000) / 10 
        },
        toPercent(num, denom) {
            let perc = num / (denom)
            return Math.round(perc * 1000) / 10 
        }        
    }

  

  
  }
  </script>
  