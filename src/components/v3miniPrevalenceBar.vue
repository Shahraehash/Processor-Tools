<template>
    <div>
      <div v-if="describe != null" class="mt-5">
          <div class="overline">Prevalence of Classes from Single Dataset</div>
          
          <!-- Dynamic class prevalence bars -->
          <div style="width:100%; height: 32px; white-space: nowrap;" >
            <div
                v-for="(cls, index) in uniqueClasses"
                :key="'class-' + cls"
                class="group-box data-set-box"
                v-bind:style="{
                  background: getClassColor(index, true),
                  width: describe.total.percent[cls] + '%'
                  }"
                >
                Class {{cls}}: {{mxRoundValue(describe.total.percent[cls])}}%
            </div>
          </div>
          
          <!-- Dynamic missing data visualization -->
          <div style="width:100%; white-space: nowrap;" class="caption">
            <div
                v-for="(cls, index) in uniqueClasses"
                :key="'missing-' + cls"
                class="group-box class-box"
                v-bind:style="{
                  background: getClassColor(index, false),
                  width: describe.non_nan.percent[cls] + '%'
                  }"
                >
                <span v-if="describe.nan.counts[cls] > 0" class="missing-text">
                  {{describe.nan.percent[cls]}}% ({{describe.nan.counts[cls]}}) missing
                </span>
                <span v-else class="missing-text">
                  No missing
                </span>
                
                <!-- Missing data overlay -->
                <div
                    class="missing-overlay"
                    v-bind:style="{
                      background: mxBarColors.missing,
                      width: describe.nan.percent[cls] + '%',
                      opacity: 0.8
                      }"
                    >
                </div>
            </div>
          </div>
          
          <div class="mt-2 caption grey--text">
            Total classes: {{uniqueClasses.length}} ({{uniqueClasses.join(', ')}})
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
      },
      
      uniqueClasses() {
        if (this.describe && this.describe.unique_classes) {
          return [...this.describe.unique_classes].sort((a, b) => a - b);
        }
        return [0, 1]; // fallback for legacy data
      }
    },
    
    mounted() {
      console.log('DEBUG: v3miniPrevalenceBar mounted');
      console.log('DEBUG: describe:', this.describe);
      console.log('DEBUG: uniqueClasses:', this.uniqueClasses);
    },
    
    methods: {
      getClassColor(index, isLight = false) {
        // Generate different colors for each class
        const colors = [
          isLight ? this.mxBarColors.classZeroLight : this.mxBarColors.classZero,
          isLight ? this.mxBarColors.classOneLight : this.mxBarColors.classOne,
          isLight ? '#FFB3B3' : '#FF6B6B', // Light/Dark Red
          isLight ? '#B3E5E0' : '#4ECDC4', // Light/Dark Teal
          isLight ? '#B3D9F2' : '#45B7D1', // Light/Dark Blue
          isLight ? '#D4E6D4' : '#96CEB4', // Light/Dark Green
          isLight ? '#FFF2CC' : '#FFEAA7', // Light/Dark Yellow
          isLight ? '#F0E6F0' : '#DDA0DD', // Light/Dark Plum
          isLight ? '#E6F7F1' : '#98D8C8', // Light/Dark Mint
          isLight ? '#FDF4E3' : '#F7DC6F'  // Light/Dark Light Yellow
        ];
        return colors[index % colors.length];
      }
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
.missing-overlay {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 2;
    height: 100%;
}
.missing-text {
    position: relative;
    z-index: 3;
    font-size: 12px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
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
