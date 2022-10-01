<template>
    <div>
        <v3miniTrainTestLabel />
        <v3miniValidate />
        {{analysis}}

        <v-select outlined dense width="50px" style="display: inline-flex; width: 80px;"></v-select>
   
    </div>

</template>
<script>
import v3miniValidate from './v3miniValidate.vue'
import v3miniTrainTestLabel from './v3miniTrainTestLabel.vue'

export default {
    name: 'v3subFileValidate',
    components: {
        v3miniValidate,
        v3miniTrainTestLabel
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
            transform: null
        }
    },
    mounted() {
        this.update()
    },
    watch: {
        analysis: () => {
            this.update()
        }
    },
    computed: {
        complete() {
            return true
        },        
    },
    methods: {
        buildTransform() {
            return {
                type: 'columnPrune',
                data: {
                    columnsToRemove: []
                }
            }
        },
        update() {
            let result = {
                complete: this.complete,
                transform: this.buildTransform()
            }

            this.$emit('update', result)
        },
   
    }
}
</script>
<style scoped>
</style>