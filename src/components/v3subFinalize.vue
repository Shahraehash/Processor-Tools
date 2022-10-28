<template>
    <div>
        <v-row dense>
            <v-col cols="6">
                <div class="overline">Original</div>
                <v-card outlined v-for="(original, originalKey) in files[0]" :key="originalKey">
                    <v3miniFileInfo :fileInfo="original"/>
                </v-card>
                
            </v-col>
            <v-col cols="6">
                <div class="overline">Current</div>
                <v-card outlined v-for="(current, currentKey) in currentFiles" :key="currentKey">
                    <v3miniFileInfo :fileInfo="current"/>
                </v-card>             
            </v-col>                
        </v-row>

        <v-text-field outlined label="Training File" style="display:inline-flex; width: 200px"></v-text-field>
        <v-text-field outlined label="Testing File" style="display:inline-flex; width: 200px"></v-text-field>
        



        
        <v3ButtonNext text="Finalize Files" @next="exportFiles()"/>
        
        <div v-if="analysis">

        </div>
    </div>
</template>
<script>
import FileDownload from 'js-file-download'
import JSZip from 'jszip'

import v3miniFileInfo from './v3miniFileInfo.vue'
import v3ButtonNext from './v3ButtonNext.vue'
import { exportFileArray } from '@/v3Methods'


export default {
    name: 'v3subFinalize',
    components: {
        v3miniFileInfo,
        v3ButtonNext

    },
    props: {
        currentFiles: {
            type: Array,
            default: () => []
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
        async exportFiles() {
            let fileObjects = await exportFileArray(this.currentFiles)
            let zip = new JSZip()
            fileObjects.forEach(fileObj => {
                zip.file(fileObj.name, fileObj.content)
            })
            let download = await zip.generateAsync({type:"blob"})
            FileDownload(download, 'milo-ready-files.zip')
        }
    }
}
</script>
<style scoped>

</style>