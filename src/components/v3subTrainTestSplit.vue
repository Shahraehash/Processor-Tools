<template>
    <div>
        <div v-if="analysis">
            <div v-if="Object.keys(analysis.fileAnalysisDict).includes('combined')">
                You only have a single data set. To prepare for use with MILO you need to split your data into a training data set and a generalization testing data set used to evaluate your model.
                <v3miniPrevalenceBar :metadata="analysis.fileAnalysisDict['combined']" class="mb-5"/>
                <v3miniSplitBar 
                    :metadata="analysis.fileAnalysisDict['combined']['segments']" 
                    :describe="analysis.fileAnalysisDict['combined']['describe']" 
                    :effectMetadata="effect"
                    @effect="applyEffect($event)"
                    class="mb-5"/>
            </div>
        </div>
    </div>
</template>
<script>
import { effectFileArray, buildTransformObject } from '@/v3Methods'

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
            effect: null
        }
    },
    mounted() {
        this.effect = this.analysis.fileAnalysisDict['combined']['segments'] //set initial effect
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