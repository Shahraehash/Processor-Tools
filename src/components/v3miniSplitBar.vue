<template>
    <div>
      <div class="overline">Allocation of Data</div>

      <div style="width:100%">

        <div
            class="title-box"
            v-bind:style="{
              background: '#2196F3',
              width:  '45%'
              }"
              
            >
            Training
        </div>
        <div
            class="title-box"
            v-bind:style="{
              background: '#9C27B0',
              width:  '45%'
              }"
            >
            Generalization Testing
        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: 'white',
              width:  '10%'
              }"
              
            >
        </div>        
      </div>

      <div style="width:100%">     
        <div
            class="title-box"
            v-bind:style="{
              background: '#009688',
              width:  '22.5%'
              }"
              
            >
        </div>
        <div
            class="title-box caption"
            v-bind:style="{
              background: '#4CAF50',
              width:  '22.5%'
              }"
              
            >
    

        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: '#009688',
              width:  '22.5%'
              }"
            >
        </div>   
        <div
            class="title-box caption"
            v-bind:style="{
              background: '#4CAF50',
              width:   '22.5%' 
              }"
            >

             
        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: 'grey',
              width:  '10%'
              }"
              
            >
        </div>   
      </div>      



  
    </div>
  
  </template>
  <script>


  export default {
    name: 'v3miniSplitBar',
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
  