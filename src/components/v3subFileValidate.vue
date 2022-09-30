<template>
    <div>
        <!-- Per File Target Validation -->
        <div>
            <div class="overline">Target Validation</div>
            <v-row>
                <v-col cols="4" v-for="(file, key) in currentFiles" :key="key">
                    
                    <v-card outlined class="pa-3">
                        <div>
                            <strong>{{file.name}}</strong>
                        </div>
                        
                        {{analysis.targetValuesArray[key]}}
                    </v-card>
               

                </v-col>
            </v-row>
            <div >


            </div>

        </div>
        <!-- File Cross Validation -->
        <div>
            <div class="overline">File Cross Validation</div>
            {{analysis.mismatchedColumns}}
        </div>
        <!-- Target Encoding -->
        <div>
            <div class="overline">Target Encoding</div>
            {{target}}
        </div>

    </div>

</template>
<script>
export default {
    name: 'v3subFileValidate',
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

        }
    }
}
</script>