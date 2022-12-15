<template>
    <div>
        <div>
            Now we'll confirm each file has a valid target and that the columns in each file match.
        </div>
        <v-row>
            <v-col cols="4">
                <!-- Per File Target Validation -->
                <div>
                    <div class="overline">Target Validation</div>
                    <v-row>
                        <v-col cols="12" v-for="(file, key) in currentFiles" :key="key">
                            
                            <v-card outlined class="pa-3" >
                                <div v-if="file.type != 'combined'" class="mb-2">
                                    <v3miniTrainTestLabel :type="file.type"/>
                                </div>
                                <div>
                                    {{file.name}} 
                                </div>
       
                                <div>
                                    <div v-if="analysis.individualValidation[key].hasTarget">
                                        <v3miniValidate :valid="true"/>
                                        Has target column
                                    </div>
                                    <div v-else>
                                        <v3miniValidate :valid="false"/>
                                        Missing target column
                                    </div>
                                </div>
                                <div>
                                    <div v-if="analysis.individualValidation[key].targetCount == 2">
                                        <v3miniValidate :valid="true"/>
                                        Has two unique values
                                    </div>
                                    <div v-else>
                                        <v3miniValidateErr :valid="false"/>

                                            Has {{analysis.individualValidation[key].targetCount}} unique value<span v-if="analysis.individualValidation[key].targetCount > 1">s</span>. Two unique values are needed for binary classification. This target is not compatible with MILO.
 
                                        
                                    </div>
                                </div>
                                <div class="ml-6">
                                    <v-chip small v-for="(item, y) in analysis.individualValidation[key].targetValues" :key="y"
                                    > {{item}} </v-chip>
                                </div>                    
                            </v-card>
                        </v-col>
                    </v-row>
                </div>                

            </v-col>
            <v-col cols="4">

                <!-- File Cross Validation -->
                <div>
                    <div class="overline">File Cross Validation</div>
                    <div>
                        <div v-if="currentFiles.length == 1">
                        <v3miniValidate :valid="true"/>
                        Only one file
                    </div>
                    <!-- Target Check -->
                    <div v-if="currentFiles.length > 1">
                        <div v-if="analysis.allTargetValues.length == 2">
                            <v3miniValidate :valid="true"/>
                            All files have target column
                        </div>
                        <div v-else>
                            <v3miniValidate :valid="false"/>
                            Values may vary between files
                        </div>
                    </div>
                    <!-- Column Check -->
                    <div v-if="currentFiles.length > 1">
                        <div v-if="analysis.mismatchedColumns.length == 0 ">
                            <v3miniValidate :valid="true"/>
                            All columns match between files
                        </div>
                        <div v-else>
                            <v3miniValidateErr :valid="false"/>
                            Columns Vary between files
                            <!-- TODO -->
                            <div v-for="(comparison, comparisonKey) in analysis.mismatchedColumns" :key="comparisonKey">
                                <div class="ma-2">
                                    <strong class="black--text">{{comparison.hasName}}</strong> has the following 
                                    columns that are missing from <strong class="red--text">{{comparison.missingName}}</strong>
                                </div>

                                <div class="px-3 py-1">
                                    <v-chip small v-for="(col, colKey) in comparison.missingCols" :key="colKey">{{col}}</v-chip>
                                </div>
                            </div>
                        </div>
                    </div>            

                    </div>


                </div>                
                        
                    </v-col>
                    <v-col cols="4">

                        <!-- Target Encoding -->
                        <!-- Hide if not two values -->
                        <div v-if="analysis.allTargetValues.length == 2">
                            <div class="overline">Target Encoding</div>
                            <div v-for="(val, cat) in analysis.targetMap" :key="cat">
                                <v-chip>{{cat}}</v-chip>
                                <v-icon>mdi-arrow-right</v-icon>
                                <v-select @change="flipValues($event, cat)" outlined dense v-model="analysis.targetMap[cat]" :items="[0,1]" style="display: inline-flex; width: 80px;"></v-select>
                            </div>
                        </div>                        
                        
                    </v-col>
                </v-row>


                <div class="mt-5">
                    We'll also check to ensure there is enough data to train and evaluate the model.
                </div>                
                <div class="overline">Sufficient Data Validation</div>

                <v3miniValidateFileSizes @validation="setSizeValidation($event)" :analysis="analysis" :currentFiles="currentFiles" :target="target" />



    </div>

</template>
<script>
import {buildTransformObject} from '@/v3Methods'


import v3miniValidate from './v3miniValidate.vue'
import v3miniValidateErr from './v3miniValidateErr.vue'
import v3miniTrainTestLabel from './v3miniTrainTestLabel.vue'
import v3miniValidateFileSizes from './v3miniValidateFileSizes.vue'

export default {
    name: 'v3subFileValidate',

    components: {
        v3miniValidate,
        v3miniValidateErr,
        v3miniTrainTestLabel,
        v3miniValidateFileSizes
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
            sizeValid: false,
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
            return this.analysis.valid && this.sizeValid
        },        
    },
    methods: {
        setSizeValidation(value) {
            console.log('sizeVaidation',value)
            this.sizeValid = value
        },
        update() {
            let result = {
                complete: this.complete,
                transformObj: buildTransformObject('file_validate_target_map', {map: this.analysis.targetMap})
            }

            this.$emit('update', result)
        },
        flipValues(val, cat) {
      //state reset
            let map = this.analysis.targetMap
            for (let i in map) {
                if (i == cat) {
                map[i] = val
                }
                else {
                map[i] = Math.abs(val - 1)
                }
            }
            this.update()
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