<template>
    <div>
        <div v-if="validation">
         
            <v-row>
                <v-col cols="6" v-for="(file, key) in currentFiles" :key="key">
                    <v-card outlined class="pa-3">
                        <div v-if="file.type != 'combined'" class="mb-2">
                            <v3miniTrainTestLabel :type="file.type"/>
                        </div>
                        <div>
                            {{file.name}} 
                        </div>
                        <!-- Train -->

                        <div >
                            
                            <!-- Valid Class Sizew -->
                            <div class="mt-3">
                                <!-- Messaging -->
                                <v3miniValidate :valid="validation[key].validMinClassSize"/>
                                {{validation[key].validMinClassSizeMessaage}}
                                
                                <!-- Table -->
                                <div>
                                    <v-simple-table class="pa-5">
                                        <template v-slot:default>
                                        <thead>
                                            <tr>
                                            <th class="text-left">
                                                Class
                                            </th>
                                            <th class="text-left">
                                                Total Rows/Samples
                                            </th>
                                            <th class="text-left">
                                                Rows Missing Data
                                            </th>
                                            <th class="text-left">
                                                Complete Rows
                                            </th>                                                                
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr
                                            v-for="(item, key) in analysis.sizeChecks[key].table" 
                                            :key="key"
                                            >
                                            <td>{{ key }}</td>
                                            <td>{{ item.total }}</td>
                                            <td>{{ item.missing }}</td>
                                            <td>{{ item.complete }}</td>
                                            </tr>
                                        </tbody>
                                        </template>
                                    </v-simple-table>
                                </div>
                            </div>

                            <!-- Valid Imputation Volume -->
                            <div v-if="file.type != 'test'">
                                <v3miniValidate :valid="validation[key].validImputationPercentage"/>
                                {{validation[key].validImputationPercentageMessaage}}
                            </div>
                        </div>    
                        
                        

                        

                            



                    </v-card>
                </v-col>
            </v-row>

        </div>
    </div>
</template>
<script>    
import v3miniValidate from './v3miniValidate.vue'
import v3miniTrainTestLabel from './v3miniTrainTestLabel.vue'

export default {
    name: 'v3miniValidateFileSizes',
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
            default: null
        },
    },
    data() {
        return {
            mxMinClassSize: 25,
            mxImputationPercentageThreshold: 0.5
        }
    },
    computed: {
        validation(){
            if (this.analysis && this.analysis.sizeChecks) {
                let result = []
                this.currentFiles.forEach((item, key) => {
                    let sizeChecks = this.analysis.sizeChecks[key]
                    if (item.type == 'train') {
                        result.push(this.validTrain(sizeChecks))
                    }
                    else if (item.type == 'test') {
                        result.push(this.validTest(sizeChecks))
                    }
                    else {
                        result.push(this.validCombined(sizeChecks))
                    }

                })
                //create array of valid min classes and evaluate each for true
                let valid = result.map(x => x.validMinClassSize).every(Boolean)

                this.$emit('validation', valid)

                return result
            }
            else {
                return null
            }
        }
    },
    methods: {
        validTrain(sizeChecks) {
            
            let validMinClassSize = sizeChecks.classMin > this.mxMinClassSize
            let validImputationPercentage = sizeChecks.rowMissingPercent < this.mxImputationPercentageThreshold 

            let validMinClassSizeMessaage = validMinClassSize ? 
                `Minimum class size of ${this.mxMinClassSize} met. ` : 
                `Minimum class size of ${this.mxMinClassSize} not met. There is insufficient data to use MILO`

            let validImputationPercentageMessaage = validImputationPercentage ?
                `Some of the data will requiring imputing or removal.` :
                `More than the recommended amount (${this.mxImputationPercentageThreshold * 100}%) of your data will requiring imputing. We don't recommend this.`


            return {
                validMinClassSize, 
                validMinClassSizeMessaage, 
                validImputationPercentage, 
                validImputationPercentageMessaage,
                type:'combined'
            }            
        },
        validTest(sizeChecks) {
            let validMinClassSize = sizeChecks.classCompleteMin > this.mxMinClassSize

            let validMinClassSizeMessaage = validMinClassSize ? 
                `Minimum class size of ${this.mxMinClassSize} with complete data met` : 
                `Minimum class size of ${this.mxMinClassSize} with complete data not met`
            
            
            return {
                validMinClassSize, 
                validMinClassSizeMessaage, 
                type:'combined'
            }
        },
        validCombined(sizeChecks) {
            let validMinClassSize = sizeChecks.classCompleteMin > this.mxMinClassSize && sizeChecks.classMin > this.mxMinClassSize * 2
            let validImputationPercentage = sizeChecks.rowMissingPercent < this.mxImputationPercentageThreshold 

            let validMinClassSizeMessaage = validMinClassSize ? 
                `Minimum class size of ${this.mxMinClassSize * 2} met` : 
                `Minimum class size of ${this.mxMinClassSize * 2} not met. The data set must include at least 25 samples per class for training initial validation and at least ${this.mxMinClassSize} samples per class with complete data for generalization testing`

                let validImputationPercentageMessaage = validImputationPercentage ?
                `Some of the data will requiring imputing or removal.` :
                `More than the recommended amount (${this.mxImputationPercentageThreshold * 100}%) of your data will requiring imputing. We don't recommend this.`


            return {
                validMinClassSize, 
                validMinClassSizeMessaage, 
                validImputationPercentage, 
                validImputationPercentageMessaage,
                type:'combined'
            }
        }
    }

}
</script>
<style scoped>

</style>