<template>
    <div>
      <div class="overline">Prevalance of Classes and Rows with Missing Data</div>

      <div style="width:100%">
        <div
            class="title-box"
            v-bind:style="{
              background: '#009688',
              width:  metadata.describe.total.percent[0] + '%'
              }"
              
            >
            Class 0:{{metadata.describe.total.percent[0]}}%
        </div>
        <div
            class="title-box"
            v-bind:style="{
              background: '#4CAF50',
              width:  metadata.describe.total.percent[1] + '%'
              }"
            >
            Class 1: {{metadata.describe.total.percent[1]}}%
        </div>        
      </div>

      <div style="width:100%">
        <div
            class="title-box"
            v-bind:style="{
              background: '#4DB6AC',
              width:  metadata.describe.nan.percent[0] + '%'
              }"
              
            >
        </div>
        <div
            class="title-box caption"
            v-bind:style="{
              background: '#00796B',
              width:  metadata.describe.non_nan.percent[0] + '%'
              }"
              
            >
            <span v-if="metadata.describe.nan.counts[0] > 0">
              ← {{metadata.describe.nan.percent[0]}}% ({{metadata.describe.nan.counts[0]}} rows) missing data
            </span>
            <span v-else>
              No missing data
            </span>            

        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: '#81C784',
              width:  metadata.describe.nan.percent[1] + '%'
              }"
            >
        </div>   
        <div
            class="title-box caption"
            v-bind:style="{
              background: '#388E3C',
              width:  metadata.describe.non_nan.percent[1] + '%' 
              }"
            >
            <span v-if="metadata.describe.nan.counts[1] > 0">
              ← {{metadata.describe.nan.percent[1]}}% ({{metadata.describe.nan.counts[1]}} rows) missing data
            </span>
            <span v-else>
              No missing data
            </span>
             
        </div>        
      </div>      



  
    </div>
  
  </template>
  <script>


  export default {
    name: 'ClassGroupBar',
    props: 
      {
        metadata: {
          type: Object,
          required: true
        }
    },
    data() {

    },
    computed: {

    },
    mounted() {

  
  
    },
    methods: {
    
  
    }
  
  }
  </script>
  