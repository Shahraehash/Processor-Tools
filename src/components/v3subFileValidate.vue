<template>
    <div>
        Test
        <v-card>
            {{analysis}}
        </v-card>
        <v-card>
            {{target}}
        </v-card>

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
}
</script>