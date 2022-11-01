<template>
    <div>
        <div v-if="analysis">
            <div v-if="Object.keys(analysis.fileAnalysisDict).includes('combined')">
                To prepare for use with MILO you need to split your data into a training data set and a generalization testing data set used to evaluate your model.
                <v3miniPrevalenceBar :metadata="analysis.fileAnalysisDict['combined']" class="mb-5"/>
                <v3miniSplitBar 
                    :metadata="analysis.fileAnalysisDict['combined']['segments']" 
                    :describe="analysis.fileAnalysisDict['combined']['describe']" 
                    :effectMetadata="effect"
                    @effect="applyEffect($event)"
                    class="mb-5"/>
            </div>
            <div v-else>
                <!-- Previous validation needs to ensure will have train and test file in first step -->
                Handle missing values and unbalanced 

                
                <v-row>

                      <v-col cols="8">
                        <div class="overline">Handle Missing Values</div>
                        <v-radio-group
                            v-model="analysis.fileAnalysisDict['train'].missing_value_option"
                            
                            >
                            <v-radio label="Remove all missing values" :value="0"></v-radio>
                            <v-radio label="Keep missing values in training and impute values - note: imputation cannot be used on generlization data as it compromises the validity of the generalization" :value="1"></v-radio>
                        </v-radio-group>
                    </v-col>

                    <v-col cols="4">
                        <div class="overline">Training Equalization</div>
                        <v-radio-group
                            >
                            <v-radio label="Downsample Major Class" :value="0"></v-radio>
                            <v-radio label="Upsample Minor Class" :value="1"></v-radio>
                        </v-radio-group>
                    </v-col>  

                </v-row>
                <v3miniTrainTestBar 
                    :train="analysis.fileAnalysisDict['train']"
                    :test="analysis.fileAnalysisDict['test']"
                    />
               


                

            </div>
        </div>
    </div>
</template>
<script>
import { effectFileArray, buildTransformObject } from '@/v3Methods'

import v3miniPrevalenceBar from '@/components/v3miniPrevalenceBar'
import v3miniSplitBar from '@/components/v3miniSplitBar'

import v3miniTrainTestBar from './v3miniTrainTestBar.vue'

export default {
    name: 'v3subFileValidate',
    components: {
        v3miniPrevalenceBar,
        v3miniSplitBar,
        v3miniTrainTestBar
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
            effect: null
        }
    },
    mounted() {
        if (this.analysis.fileAnalysisDict['combined']) {
            this.effect = this.analysis.fileAnalysisDict['combined']['segments'] //set initial effect
        }
        
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
                transformObj: buildTransformObject('train_test_split_impute', this.effect)
            }
            this.$emit('update', result)
        },
        applyEffect(effectParams) {
            let effectObj = {
                method: 'train_test_split_impute',
                ...effectParams
            }

            console.log(effectObj)

            effectFileArray(this.currentFiles, this.target, effectObj).then((result) => {
                this.effect = result
                this.update()
            })
            
        }        
       
   
    }
}
</script>
<style scoped>

</style>