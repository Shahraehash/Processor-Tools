<template>
    <div>
        <div v-if="analysis">
            <div v-if="analysis.fileAnalysisCombined.length == 0" class="ma-5">
                <v3miniValidate :valid="true"/> No columns need encoding.
            </div>
            <div v-else>


                <v3miniValidate :valid="false"/>{{ analysis.fileAnalysisCombined.length}} columns need adjusting
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
                                <v-chip>{{column.name}}</v-chip>
                            </div>
                            <div>
                                {{column.method}}
                            </div>  
                            <div>
                                Unique: {{column.unique_values}}
                            </div>  
                            <div>
                                Nan: {{column.nan_row_index}}
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