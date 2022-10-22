<template>
    <div>

      <v-row>
                    <v-col cols="8">
                        <div class="overline">Handle Missing Values</div>
                        <v-radio-group
                            v-model="missingValuesSetting"
                            >
                            <v-radio label="Drop all missing values" :value="0"></v-radio>
                            <v-radio label="Put missing values in the training set and impute them" :value="1"></v-radio>
                        </v-radio-group>
                    </v-col>

                    <v-col cols="4">
                        <div class="overline">Handle Prevlence in Generalization Set</div>
                        <v-radio-group
                            v-model="prevalenceSetting"
                            
                            >
                            <v-radio label="Maintain Original Prevlence" :value="0"></v-radio>
                            <v-radio label="Adjust based on Data Change" :value="1"></v-radio>
                        </v-radio-group>
                    </v-col>                
                    <v-col cols="12">
                        <div class="overline">Set size of training data</div>
                        <v-slider
                            v-model="trainingSize"
                            :max="200"
                            :min="25"
                            :step="1"
                            :ticks="true"
                            :thumb-label="true"
                            thumb-color="primary"
                            track-color="primary"
                            tick-size="4"
                            >
                        </v-slider>

                    </v-col>                       
                </v-row>

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
      return {
        missingValuesSetting: 0,
        prevalenceSetting: 0,
        trainingSize: 25        

      }

    },
    computed: {


    },
    mounted() {

  
  
    },
    methods: {
    
  
    }
  
  }
  </script>
  