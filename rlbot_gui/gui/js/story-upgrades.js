export default {
    name: 'story-upgrades',
    props: {
        currency: 0,
        upgradeSaveState: Object,
        upgrades: Object
    },
    template: /*html*/`
    <b-list-group>
        <b-list-group-item 
            v-for="upgrade in upgrades_ui"
            class="d-flex justify-content-between align-items-center"
            v-bind:variant="upgrade.purchased ? 'success' : upgrade.available ? 'default' : 'dark'">
            {{upgrade.text}}
            <b-button v-if="!upgrade.purchased"
                v-bind:id="upgrade.id"
                variant="success"
                v-bind:disabled="!upgrade.available"
                @click="purchase(upgrade)">
                {{upgrade.cost}}
                <b-img src="imgs/story/coin.png" height="30px"/>
            </b-button>
        </b-list-group-item>
    </b-list-group>
    `,
    computed: {
        upgrades_ui: function () {
            let currency = this.currency;
            let result = this.upgrades.map((item) => ({
                id: item.id,
                text: item.text,
                cost: item.cost,
                prereqs: item.prereqs,
                purchased: Boolean(this.upgradeSaveState[item.id])
            }));

            result.forEach((item) => (
                item.available = currency >= item.cost && (!item.prereqs || item.prereqs.length == 0 || (item.prereqs && result.every((other_item) => (
                    item.prereqs.includes(other_item.id) ? other_item.purchased : true
                ))))
            ))

            return result;
        },
    },
    methods: {
        purchase: function (item) {
            console.log("In purchases", item.id);
            this.$emit('purchase_upgrade', {
                id: item.id,
                currentCurrency: this.currency,
                cost: item.cost
            });
        }
    }
};