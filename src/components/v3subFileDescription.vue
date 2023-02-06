<template>
    <div>
        Review the data descriptions of each file below.


        <v-card
            v-for="(file, x) in analysis"
            :key="x"
            class="my-3"
            flat outlined
            >
        <div class="pa-3" @click="showTable = !showTable">
            <v-btn icon tile color=""><v-icon>mdi-chart-bar</v-icon></v-btn>
            {{ file.name }}
        </div>



            <v-data-table

                :headers="[
                {text: 'Column', value:'feature'},
                {text: 'Count', value:'count'},
                {text: 'Mean', value:'mean'},
                {text: 'STDEV', value:'std'},
                {text: 'Min', value:'min'},
                {text: '25%', value:'25%'},
                {text: '50%', value:'50%'},
                {text: '75%', value:'75%'},
                {text: 'Max', value:'max'},
                {text: 'Skew', value:'skew'},
                ]"
                :items="file.describe"
                class="elevation-1"
            >
            </v-data-table>

        </v-card>        


    </div>

</template>
<script>
import {buildTransformObject} from '@/v3Methods'

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
            type: Array,
            default: () => {}
        },
    },
    data() {
        return {

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

        update() {
            let result = {
                complete: this.complete,
                transformObj: buildTransformObject('pass_file_no_change', null)
            }

            this.$emit('update', result)
        },       
    }
}
</script>
<style scoped>
.small-select {
    display: inline;
    width: 100px
}    
</style>