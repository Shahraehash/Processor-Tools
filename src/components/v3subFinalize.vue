<template>
    <div>
        <v-card class="pa-10" outlined>Placeholder for file diff from start to end</v-card>
        <div v-if="analysis">

        </div>
    </div>
</template>
<script>
import { effectFileArray, buildTransformObject } from '@/v3Methods'



export default {
    name: 'v3subFinalize',
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
                transformObj: buildTransformObject('finalize', this.effect)
            }
            this.$emit('update', result)
        },
        applyEffect(effectParams) {
            let effectObj = {
                method: 'finalize',
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