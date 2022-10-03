<template>
    <div>
        <v3miniTrainTestLabel />
        <v3miniValidate />
        <div>All datasets are combined for this analysis. The effect or removing a column is shown by file below.</div>
        <div v-if="analysis">
            <v-row dense>
                <v-col cols="6">
                    
                    <div class="text-center overline">Select Columns for Removal</div>

                    
                    <v-card class="mx-3 pa-1" flat>
                        <v-row>
                            <v-col cols="3">
                            </v-col>
                            <v-col cols="3" class="text-center">
                                <div class="caption">Rows with only this column missing</div>
                            </v-col>
                            <v-col cols="3" class="text-center">
                                <div class="caption">Rows with multiple columns missing</div>
                            </v-col>
                            <v-col cols="3" class="text-center">
                                <div class="caption">% Contribution of Missing Cells</div>
                            </v-col>   
                        </v-row>
                    </v-card>
                    <v-card
                         @click="selection(item.col)"
                        class="ma-3 pa-1"
                        v-bind:class="{selected: selectedColumns.includes(item.col)}"
                        
                         v-for="(item, key) in analysis.fileAnalysisCombined" :key="key">


                        <v-row dense>
                            <v-col cols="1" style="text-decoration: none!important;">
                                <v-icon v-if="selectedColumns.includes(item.col)">mdi-checkbox-marked</v-icon>
                                <v-icon v-else>mdi-checkbox-blank-outline</v-icon>
                            </v-col>
                            <v-col cols="4">
                                <v-chip>{{item.col}}</v-chip>
                            </v-col>
                            <v-col cols="2" class="text-center">
                                {{item.singleMissing}}
                            </v-col>
                            <v-col cols="2" class="text-center">
                                {{item.multipleMissing}}
                            </v-col>
                            <v-col cols="2" class="text-center">
                                {{item.percentContributions}}%
                            </v-col>                                                                           
                        </v-row>
                    
                    </v-card>

                </v-col>
                <v-col cols="6">
                    <div class="text-center overline">Summary of Missing Values</div>


                    <apexchart v-if="graphOptions && graphSeries" width="80%"  type="donut" :options="graphOptions" :series="graphSeries"></apexchart>
                    <div v-if="effect">
                        <v-card v-for="(fileEffect, key) in effect.fileEffectArray" :key="key"> 
                        {{currentFiles[key].name}}
                        <div>>
                            Rows with Missing Data: {{fileEffect.old.missing.rows}} => {{fileEffect.new.missing.rows}}
                        </div>                                             

                        
                        </v-card>>

                    </div>



                    

                </v-col>            
            </v-row>
        
        
        </div>




        <v-select outlined dense width="50px" style="display: inline-flex; width: 80px;"></v-select>
   
    </div>

</template>
<script>
import { effectFileArray, buildTransformObject } from '@/v3Methods'


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
            transform: null,
            selectedColumns: [],
            graphOptions: null,
            graphSeries: null,
            effect: null,
        }
    },
    mounted() {
        this.update()
        let labels = this.analysis.fileAnalysisCombined.map(x => x.col)
        this.graphOptions = this.makeGraphOptions(labels)
        this.graphSeries = this.analysis.fileAnalysisCombined.map(x => x.percentContributions)
        
    },
    watch: {
        analysis: () => {
            this.update()

        },
        selectedColumns: function(val) {
            let effect = {
                method: 'column_removal',
                selectedColumns: val
            }
            effectFileArray(this.currentFiles, this.target, effect).then((res) => {
                this.effect = res
            })

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
                transformObj: buildTransformObject('column_removal', {selectedColumns: this.selectedColumns})
            }

            this.$emit('update', result)
        },        
        selection(value) {
            this.selectedColumns.includes(value) ? this.selectedColumns.splice(this.selectedColumns.indexOf(value), 1) : this.selectedColumns.push(value)
            this.update()
        },
        makeGraphOptions(labels) {
            return {
                colors: [
                '#4c86ff',
                '#577df9',
                '#6173f3',
                '#6b69ec',
                '#745ee4',
                '#7d53db',
                '#8446d2',
                '#8b38c8',
                '#9225bd',
                '#9229b1',
                ],
                labels: labels,
                chart: {
                    animations: {
                        enabled: true
                    },
                    events: {
                        dataPointSelection: (event, chartContext, config) => {
                            event, chartContext, config
                            this.selection(this.graphOptions.labels[config.dataPointIndex])
                        }
                    }
                },

                dataLabels: {
                enabled: false
                },

                plotOptions: {
                }
            }
        },        
   
    }
}
</script>
<style scoped>
.selected {
    background: rgb(234, 234, 234);
    text-decoration: line-through;
}
</style>