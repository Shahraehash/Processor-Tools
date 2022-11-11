<template>
    <div>
        <v3StepHeading
        style="display: inline-flex;"
        :stepNumber="stepNumber"
        :stepTitle="stepTitle"
        />

        <v-btn @click="$emit('removeComponent')" class="float-right" text v-if="optional" style="display: inline-flex;">
          Remove Step
          <v-icon >mdi-close</v-icon>
        </v-btn>  


        <v-row dense wrap>
            <v-col cols="4">
                <div class="overline ml-4">Summary</div>
                <v-card outlined class="pa-3 ma-2">
                    <v3miniFilesDelta :originalArray="originalFiles" :finalArray="finalFilesOnlyTrainTest"/>        
                </v-card>
            </v-col>
            <v-col cols="3">
                <div class="overline ml-4">Original</div>
                <v-card outlined class="pa-3 ma-2" v-for="(original, originalKey) in originalFiles" :key="originalKey">
                    <v3miniFileInfo :fileInfo="original"/>
                </v-card>
                
            </v-col>
            <v-col cols="3">
                <div class="overline ml-4">Current</div>
                <v-card outlined class="pa-3 ma-2" v-for="(current, currentKey) in finalFilesOnlyTrainTest" :key="currentKey">
                    <v3miniFileInfo :fileInfo="current"/>
                </v-card>             
            </v-col>    
     
            <v-col cols="2" v-if="otherFiles.length > 0">
                <div class="overline ml-4">Unused/Other</div>
                <v-card disabled="true" outlined class="pa-3 ma-2" v-for="(current, currentKey) in otherFiles" :key="currentKey">
                    <v3miniFileInfo :fileInfo="current"/>
                </v-card>             
            </v-col>                                    
        </v-row>

        <!-- <v-text-field outlined label="Training File" style="display:inline-flex; width: 200px"></v-text-field>
        <v-text-field outlined label="Testing File" style="display:inline-flex; width: 200px"></v-text-field> -->
        



        
        <div class="text-right" v-if="files.length > 0">
            <v3ButtonNext 
            @next="exportFiles"
            text="Finalize Files"
        />

    </div>    
        
        <div v-if="analysis">

        </div>
    </div>
</template>
<script>
import v3StepHeading from '@/components/v3StepHeading'  
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

import v3miniFilesDelta from '@/components/v3miniFilesDelta'
import v3miniFileInfo from './v3miniFileInfo.vue'
import v3ButtonNext from './v3ButtonNext.vue'
import { exportFileArray } from '@/v3Methods'


export default {
    name: 'v3Finalize',
    components: {
        v3StepHeading,
        v3miniFilesDelta,
        v3miniFileInfo,
        v3ButtonNext

    },
    props: {
        stepNumber: {
            type: Number || String
        },
        stepTitle: {
            type: String
        },
        optional: {
            type: Boolean,
            default: false
        },          
        files: {
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

        
    },
    watch: {

    },
    computed: {
        originalFiles() {
            return this.files[0]
        },
        finalFiles() {
            return this.files[this.files.length - 1]
        },
        finalFilesOnlyTrainTest() {
            return this.finalFiles.filter(file => file.type === 'train' || file.type === 'test')
        },
        otherFiles() {
            return this.finalFiles.filter(file => file.type != 'train' && file.type != 'test')
        },        

        complete() {
            return true
        },        
    },
    methods: {
        async exportFiles() {
            this.$store.commit('FileProcessingDialogLoadingSet', true)
            this.$store.commit('FileProcessingDialogOpenSet', true)

            let fileObjects = await exportFileArray(this.files[this.files.length - 1])
            let zip = new JSZip()
            fileObjects.forEach(fileObj => {
                zip.file(fileObj.name, fileObj.content)
            })
            let download = await zip.generateAsync({type:"blob"})
            
        
            //add 1 second automatic delay to UI
            const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
            await delay(1000);

            this.$store.commit('FileProcessingDialogLoadingSet', false)

            FileDownload(download, 'milo-ready-files.zip')
            
        }
            
    }
}
</script>
<style scoped>

</style>