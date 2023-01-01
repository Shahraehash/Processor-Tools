<template>
    <div>
        <div v-if="analysis">
            <div v-if="Object.keys(analysis.fileAnalysisDict).includes('combined')">
                To prepare for use with MILO you need to split your data into a training data set and a generalization testing data set used to evaluate your model.
                <v3miniTrainTestSingleFileImpute 
                    :combinedFile="analysis.fileAnalysisDict['combined']" 
                    :effectMetadata="effect"
                    @effect="setEffect($event)"
                    />


                
                <!-- <v3miniSplitBar 
                    :metadata="analysis.fileAnalysisDict['combined']['segments']" 
                    :describe="analysis.fileAnalysisDict['combined']['describe']" 
                    :effectMetadata="effect"
                    @effect="applyEffect($event)"
                    class="mb-5"/> -->
            </div>
            <div v-else>
                <!-- Previous validation needs to ensure will have train and test file in first step -->
                You already have your data allocated into two sets. We can now decide how to manage missing values in your respective data set and unbalanced training classes (if present).

                <v3miniTrainTestSeperateImpute 
                    :train="analysis.fileAnalysisDict['train']"
                    :test="analysis.fileAnalysisDict['test']"
                    @effect="setEffect($event)"
                    />
            </div>
        </div>
    </div>
</template>
<script>
import { buildTransformObject } from '@/v3Methods'

import v3miniTrainTestSingleFileImpute from './v3miniTrainTestSingleFileImpute.vue'
// import v3miniSplitBar from '@/components/v3miniSplitBar'
import v3miniTrainTestSeperateImpute from './v3miniTrainTestSeperateImpute.vue'

export default {
    name: 'v3subFileValidate',
    components: {
        v3miniTrainTestSingleFileImpute,
        // v3miniSplitBar,
        v3miniTrainTestSeperateImpute
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
            console.log(result)     
            this.$emit('update', result)
        },
        setEffect(effectParams) {
            //Does not rquire backend calculation, only priming data for transform
            let effectObj = {
                method: 'train_test_split_impute',
                ...effectParams
            }
            this.effect = effectObj
            this.update()
                   
        }        
       
   
    }
}
</script>
<style scoped>

</style>