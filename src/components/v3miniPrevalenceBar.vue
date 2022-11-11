<template>
    <div>
      <div v-if="describe != null" class="mt-5">
          <div class="overline">Prevalance of Classes from Single Dataset</div>
          <div style="width:100%; height: 32px;" >
            <div
                class="group-box data-set-box"
                v-bind:style="{
                  background: mxBarColors.classZeroLight,
                  width:  describe.total.percent[0] + '%'
                  }"
                  
                >
                Class 0: {{mxRoundValue(describe.total.percent[0])}}%
            </div>

            <div
                class="group-box data-set-box"
                v-bind:style="{
                  background: mxBarColors.classOneLight,
                  width:  describe.total.percent[1] + '%'
                  }"
                >
                Class 1: {{mxRoundValue(describe.total.percent[1])}}%
            </div>        
          </div>
          <div style="width:100%" class="caption">
            <div
                class="group-box class-box"
                v-bind:style="{
                  background: mxBarColors.missing,
                  width:  describe.nan.percent[0] + '%'
                  }"
                  
                >
            </div>
            <div
                class="group-box class-box"
                v-bind:style="{
                  background: mxBarColors.classZero,
                  width:  describe.non_nan.percent[0] + '%'
                  }"
                v-bind:class="{
                  'text-left': describe.nan.counts[0] > 0
                }"  
                >
                
                <span v-if="describe.nan.counts[0] > 0">
                  ← {{describe.nan.percent[0]}}% ({{describe.nan.counts[0]}} rows) missing data
                </span>
                  <span v-else>
                    No missing data
                  </span>            

            </div>               
            <!-- Class 1 Missing -->
            <div
                class="group-box class-box"
                v-bind:style="{
                  background: mxBarColors.missing,
                  width:  describe.nan.percent[1] + '%'
                  }"
                  
                >
            </div>
            <div
                class="group-box class-box"
                v-bind:style="{
                  background: mxBarColors.classOne,
                  width:  describe.non_nan.percent[1] + '%'
                  }"
                v-bind:class="{
                  'text-left pl-2': describe.nan.counts[1] > 0
                }"                    
                  
                >
                <span v-if="describe.nan.counts[1] > 0">
                  ← {{describe.nan.percent[1]}}% ({{describe.nan.counts[1]}} rows) missing data
                </span>
                  <span v-else>
                    No missing data
                  </span>            
            </div>              
          </div>          
      </div>
    </div>
  
  </template>
  <script>

  import v3Mixin from '@/components/v3Mixin';

  export default {
    name: 'v3miniPrevalenceBar',
    mixins: [v3Mixin],
    props: 
      {
        combinedFile: {
          type: Object,
          required: true
        }
    },
    data() {
      return {
        
      }

    },
    computed: {
      describe() {
        if (this.combinedFile != null) {
          return this.combinedFile.describe
        }
        else {
          return null
        }
        
      }

    },
    mounted() {

  
  
    },
    methods: {
    
  
    }
  
  }
</script>

<style scoped>
.data-set-box {
    padding-top: 5px;
    height:32px;

}
.class-box {
    padding-top: 10px;
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
  