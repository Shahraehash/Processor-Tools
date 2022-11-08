<template>
    <div>
        <div v-if="graphObject">
            <div>
                <div class="key-box" 
                     v-bind:style="{
                        background: mxBarColors.missing,
                    }">    
                </div>
                <div v-bind:style="{
                        display: 'inline-block',
                    }">    
                    Missing
                </div>

                <div class="key-box"
                      v-bind:style="{
                        background: mxBarColors.blank,
    
                    }">    
                </div>
                <div
 
                    v-bind:style="{
                        display: 'inline-block',
                        
                    }">    
                    Removed
                </div>
                            

            </div>
            <div style="width:100%; height: 40px;" >
            <div
                class="group-box data-set-box right-spacer"
                v-bind:style="{
                background: mxBarColors.train,
                width:  graphObject.train.percent[0] + graphObject.train.percent[1] + '%',

                }"
                >
                Training and Initial Validation File
            </div>
            <div
                class="group-box data-set-box right-spacer"
                v-bind:style="{
                background: mxBarColors.test,
                width:  graphObject.test.percent[0] + graphObject.test.percent[1] + '%',

                }"
                >
                Generalization Testing File
            </div>        
            <div
                class="group-box data-set-box "
                v-bind:style="{
                background: mxBarColors.blank,
                width: graphObject.remainder.percent + '%',
                }"
                
                >
                Removed
            </div>        
            </div>

            <div style="width:100%">     
            <div
                class="group-box class-box "
                v-bind:style="{
                background: mxBarColors.classZero,
                width:  graphObject.train.percent[0] + '%',

                }"
                
                >
                <div class="missing class-box"
                    v-bind:style="{
                    background: mxBarColors.missing,
                    width: graphObject.train.missingPercent[0] +'%'
                    }"
                ></div>                
                Class 0: {{graphObject.train.counts[0]}}
            </div>
            <div
                class="group-box class-box right-spacer"
                v-bind:style="{
                background: mxBarColors.classOne,
                width:  graphObject.train.percent[1] + '%',

                }"
                >
                <div class="missing class-box"
                    v-bind:style="{
                    background: mxBarColors.missing,
                    width: graphObject.train.missingPercent[1] + '%'
                    }"
                ></div>
                Class 1: {{graphObject.train.counts[1]}}
            </div>        
            <div
                class="group-box class-box"
                v-bind:style="{
                background: mxBarColors.classZero,
                width:  graphObject.test.percent[0] +'%',

                }"
                >
                <div class="missing class-box"
                    v-bind:style="{
                    background: mxBarColors.missing,
                    width: graphObject.test.missingPercent[0] +'%'
                    }"
                ></div>
                Class 0: {{graphObject.test.counts[0]}}
            </div>   
            <div
                class="group-box class-box right-spacer"
                v-bind:style="{
                background: mxBarColors.classOne,
                width: graphObject.test.percent[1] + '%',

                }"
                >
                Class 1: {{graphObject.test.counts[1]}}
                <div class="missing class-box"
                    v-bind:style="{
                    background: mxBarColors.missing,
                    width: graphObject.test.missingPercent[1] + '%'
                    }"
                ></div>
                
            </div>        
            <div
                class="group-box class-box "
                v-bind:style="{
                background: mxBarColors.blank,
                width: graphObject.remainder.percent + '%'
                }"
                
                >

                {{graphObject.remainder.count}}
            </div>   
        </div>            
        </div>
    </div>
  
  </template>
  <script>
  import v3Mixin from '@/components/v3Mixin';

  export default {
    name: 'v3miniTrainTestBar',
    mixins: [v3Mixin],
    props: 
      {
        graphObject: {
          type: Object,
          required: true
        },
          

   
    },
    watch: {

    },
    data() {
      return {

      }

    },
    computed: {


    },
    created() {

    },
    mounted() {

    },

  
  
    methods: {

    
  
    }
  
  }
  </script>

    <style scoped>
    
    .data-set-box {
        padding-top: 8px;
        height:40px;
    }
    .class-box {
        padding-top: 8px;
        height:40px;
    }
    .group-box {
        box-sizing: ;
        position: relative;
        transition: width 0.5s;
        display: inline-block;
        text-align: center;
        color: white;
        overflow: hidden;
    }
    .right-spacer {
        border-right: 5px white solid;
    }
    .missing {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1;
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
  