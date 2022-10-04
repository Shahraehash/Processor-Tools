<template>
    <div>
        <div>Pick which data you want...</div>
        <div v-if="analysis">
            {{analysis}}
           
        </div>
    </div>
</template>
<script>
import { buildTransformObject } from '@/v3Methods'



export default {
    name: 'v3subFileValidate',
    components: {

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