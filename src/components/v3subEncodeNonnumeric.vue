<template>
    <div>
        <div v-if="analysis">
            <div v-if="analysis.fileAnalysisCombined.length == 0" class="ma-5">
                <v3miniValidate :valid="true"/> No columns need encoding.
            </div>
            <div v-else>
                <div class="ma-3">
                    <span class="primary--text text-h5">{{ analysis.fileAnalysisCombined.length}}</span> columns need adjusting
                </div>


                
                <v-row dense>
    
                    <v-col cols="6"
                        v-for="(column, key) in analysis.fileAnalysisCombined"
                        :key="key"
                        >
                        <v-card 
                            flat
                            outlined
                            class="ma-1 pa-3"
                            v-bind:class="{drop: column.selection == 'drop'}"
                            >


                            <div>
                                <v3miniValidate :valid="false"/>
                                Column Needing Attention: <v-chip>{{column.name}}</v-chip>
                            </div>
                            <div class="ma-3">

                                <div v-if="column.method == 'one_hot_encode'">
                                    The data in this column is <strong class="light-blue--text">categorical</strong> with the {{column.unique_values.length}} unique values: 
                                    <v-chip color="light-blue" dark small v-for="(cat, catKey) in column.unique_values" :key="catKey">{{cat}}</v-chip>. 
                                    <br>We can either convert each category to a seperate column or remove the column from the dataset. 
                                    <!-- Message if >20 categories, the drop mode is set on the backend method analyze_encode_nonnumeric -->
                                    <v-alert type="warning" text v-if="column.unique_values.length > 20">With so many categories, the increase in column number may adversely affect your dataset and we recommend you drop the column</v-alert>
                                </div>
                                <div v-if="column.method == 'mixed_to_numeric'">
                                    The data in this column is <strong class="light-blue--text">mostly numeric</strong> ({{column.values.percent}}%) with some non-numeric values. We can covert to numeric data and treat non-numeric data as missing values or remove the column from the dataset.
                                </div>                                

                            </div>   
                            <div>
                                <v-select
                                    v-model="column.selection"
                                    :items="column.items"
                                    item-value="value"
                                    item-text="text"
                                    outlined
                                    dense
                                    @change="update()"
                                    >

                                </v-select>
                            </div>                          
                        
                        </v-card>
                                                                                
                        
                    </v-col>

                </v-row>



            </div>


           
           
        </div>
    </div>
</template>
<script>
import { buildTransformObject } from '@/v3Methods'
import v3miniValidate from './v3miniValidate.vue'


export default {
    name: 'v3subFileValidate',
    components: {
        v3miniValidate

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
            localAnalysis: null // this is a copy of the analysis object, needed to make changes
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
                transformObj: buildTransformObject('encode_nonnumeric', this.analysis['fileAnalysisCombined']) //data model in analysis
            }

            this.$emit('update', result)
        },        
       
   
    }
}
</script>
<style scoped>

.drop {
    background-color: #e2e2e2;
    opacity: 0.5;
}

</style>