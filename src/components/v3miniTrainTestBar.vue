<template>
    <div>
        <div v-if="graphObject">
            <div style="width:100%" >
            <div
                class="group-box "
                v-bind:style="{
                background: '#2196F3',
                width:  graphObject.train.percent[0] + graphObject.train.percent[1] + '%'
                }"
                >
                Training
            </div>
            <div
                class="group-box "
                v-bind:style="{
                background: '#9C27B0',
                width:  graphObject.test.percent[0] + graphObject.test.percent[1] + '%'
                }"
                >
                Generalization Testing
            </div>        
            <div
                class="group-box "
                v-bind:style="{
                background: 'white',
                width: graphObject.remainder.percent + '%'
                }"
                
                >
            </div>        
            </div>

            <div style="width:100%">     
            <div
                class="group-box "
                v-bind:style="{
                background: '#009688',
                width:  graphObject.train.percent[0] + '%'
                }"
                
                >
                <div class="missing"
                    v-bind:style="{
                    width: graphObject.train.missingPercent[0] +'%'
                    }"
                ></div>                
                Class 0: {{graphObject.train.counts[0]}}
            </div>
            <div
                class="group-box "
                v-bind:style="{
                background: '#4CAF50',
                width:  graphObject.train.percent[1] + '%'
                }"
                >
                <div class="missing"
                    v-bind:style="{
                    width: graphObject.train.missingPercent[1] + '%'
                    }"
                ></div>
                Class 1: {{graphObject.train.counts[1]}}
            </div>        
            <div
                class="group-box"
                v-bind:style="{
                background: '#009688',
                width:  graphObject.test.percent[0] +'%'
                }"
                >
                <div class="missing"
                    v-bind:style="{
                    width: graphObject.test.missingPercent[0] +'%'
                    }"
                ></div>
                Class 0: {{graphObject.test.counts[0]}}
            </div>   
            <div
                class="group-box"
                v-bind:style="{
                background: '#4CAF50',
                width: graphObject.test.percent[1] + '%' 
                }"
                >
                Class 0: {{graphObject.test.counts[1]}}
                <div class="missing"
                    v-bind:style="{
                    width: graphObject.test.missingPercent[1] + '%'
                    }"
                ></div>
                
            </div>        
            <div
                class="group-box"
                v-bind:style="{
                background: 'grey',
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


  export default {
    name: 'v3miniTrainTestBar',
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

    .group-box {
        padding-top:5px;
        height: 30px;
        position: relative;
        transition: width 0.5s;
        display: inline-block;
        text-align: center;
        color: white;
        overflow: hidden;
    }
    .missing {
        position: absolute;
        top: 0;
        left: 0;
        height: 30px;
        background: orange;
        z-index: 1;
    }

  </style>
  