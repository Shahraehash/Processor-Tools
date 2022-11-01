<template>
    <div>


      <v-row>
                    <v-col cols="8">
                        <div class="overline">Handle Missing Values</div>
                        <v-radio-group
                            @change="change"
                            v-model="missingValuesOption"
                            >
                            <v-radio label="Remove missing values" :value="0"></v-radio>
                            <v-radio label="Keep missing values in training and impute values - note: imputation cannot be used on generlization data as it compromises the validity of the generalization" :value="1"></v-radio>
                        </v-radio-group>
                    </v-col>

                    <v-col cols="4">
                        <div class="overline">Handle Prevlence in Generalization Set</div>
                        <v-radio-group
                            @change="change"
                            v-model="prevalenceOption"
                            
                            >
                            <v-radio label="Use All Available Data" :value="0"></v-radio>
                            <v-radio label="Maintain Original Data Prevelence" :value="1"></v-radio>
                        </v-radio-group>
                    </v-col>                
                    <v-col cols="12">
                        <div class="overline">Set size of training data</div>
                        <v-slider
                            style="display: inline-flex; width: 200px"
                            @change="change"
                            v-model="localMetadata.train.counts[0]"
                            :max="maxTraining"
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
              width:  localMetadata.train.percent[0] + localMetadata.train.percent[1] + '%'
              }"
              
            >
            Training
        </div>
        <div
            class="title-box"
            v-bind:style="{
              background: '#9C27B0',
              width:  localMetadata.test.percent[0] + localMetadata.test.percent[1] + '%'
              }"
            >
            Generalization Testing
        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: 'white',
              width: localMetadata.remainder.percent + '%'
              }"
              
            >
        </div>        
      </div>

      <div style="width:100%">     
        <div
            class="title-box "
            v-bind:style="{
              background: '#009688',
              width:  localMetadata.train.percent[0] + '%'
              }"
              
            >
            {{localMetadata.train.counts[0]}}
        </div>
        <div
            class="title-box "
            v-bind:style="{
              background: '#4CAF50',
              width:  localMetadata.train.percent[1] + '%'
              }"
            >
            {{localMetadata.train.counts[1]}}
    

        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: '#009688',
              width:  localMetadata.test.percent[0] + '%'
              }"
            >
            {{localMetadata.test.counts[0]}}
        </div>   
        <div
            class="title-box"
            v-bind:style="{
              background: '#4CAF50',
              width: localMetadata.test.percent[1] + '%' 
              }"
            >
            {{localMetadata.test.counts[1]}}
             
        </div>        
        <div
            class="title-box"
            v-bind:style="{
              background: 'grey',
              width: localMetadata.remainder.percent + '%'
              }"
              
            >
            {{localMetadata.remainder.counts}}
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
        },
        describe: {
          type: Object,
          required: true
        },   
        effectMetadata: {
          type: Object,
          required: false
        },                
    },
    watch: {
      effectMetadata: {
        handler(newVal) {
          this.localMetadata = newVal
        },
        deep: true
      }
    },
    data() {
      return {
        missingValuesOption: 0,
        prevalenceOption: 0,  
        localMetadata: null
      }

    },
    computed: {
      maxTraining() {
        return this.describe.non_nan.counts[this.describe.minor] - 25
      },


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
  