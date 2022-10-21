<template>
    <div>
        
        <div v-if="analysis">
            

            <div v-if="Object.keys(analysis.fileAnalysisDict).includes('combined')">

                <v3miniPrevalenceBar :metadata="analysis.fileAnalysisDict['combined']" class="mb-5"/>
            
                <v-row>
                    <v-col cols="8">
                        <div class="overline">Handle Missing Values</div>
                        <v-radio-group
                            v-model="missingValuesSetting"
                            >
                            <v-radio label="Drop all missing values" :value="0"></v-radio>
                            <v-radio label="Include rows with missing values in training and impute up to 30% of training" :value="1"></v-radio>
                            <v-radio label="Include rows with missing values in training and impute all missing data" :value="2"></v-radio>

                            
                        </v-radio-group>
                    </v-col>

                    <v-col cols="4">
                        <div class="overline">Handle Prevlence of Data</div>
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
                            :max="100"
                            :min="0"
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

                <v3miniSplitBar :metadata="analysis.fileAnalysisDict['combined']" class="mb-5"/>

            
            
        
            </div>


            <div>
                {{analysis}}
            </div>


            


           
        </div>
    </div>
</template>
<script>
import { buildTransformObject } from '@/v3Methods'

import v3miniPrevalenceBar from '@/components/v3miniPrevalenceBar'
import v3miniSplitBar from '@/components/v3miniSplitBar'

export default {
    name: 'v3subFileValidate',
    components: {
        v3miniPrevalenceBar,
        v3miniSplitBar
    },
    props: {
        currentFiles: {
            type: Array,
            default: () => []
        },
        target: {
            type: String,
            default: null
        },
        analysis: {
            type: Object,
            default: () => {}
        },
    },
    data() {
        return {
            effect: null,
            missingValuesSetting: 0,
            prevalenceSetting: 0,

        }
    },
    mounted() {
        this.update()

        
    },
    watch: {
        analysis: () => {
            this.update()

        },

    },
    computed: {
        complete() {
            return true
        },        
    },
    methods: {
        update() {
            let result = {
                complete: this.complete,
                transformObj: buildTransformObject('train_test_split', {})
            }

            this.$emit('update', result)
        },        
       
   
    }
}
</script>
<style scoped>

</style>