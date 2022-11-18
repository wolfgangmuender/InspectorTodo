<template>
    <p>Hello {{ adjective }} World!</p>
    <!-- TODO IT-17 add second line -->
</template>

<script>
module.exports = {
    data: function () {
        // TODO IT-18 also support adverbs
        return {
            adjective: 'beautiful'
        }
    }
}
</script>

<style scoped>
p {
    font-size: 12px;
    text-align: left;
}
</style>
