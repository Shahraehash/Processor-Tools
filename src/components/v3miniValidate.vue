<template>
    <div class="inline-div">
        <v-icon v-if="valid" color="green">mdi-check-circle</v-icon>
        <v-icon v-else color="orange">mdi-alert-circle</v-icon>
    </div>
</template>
<script>    
export default {
    name: 'v3miniValidate',
    props: {
        valid: {
            type: Boolean,
            default: false
        },
    }
}
</script>
<style scoped>
.inline-div {
    display: inline;
}
</style>