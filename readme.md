

# What's AnyswapTelegramBot
AnyswapTelegramBot provides easy information for the users of Anyswap. Commands include:
1. APY - get ANY rewards and pool fees for differenet pools
2. MC - Marketcap info of $ANY
3. TVL - Total value locked on Anyswap
4. VOL - Trade volume on Anyswap 
# Installation
1. Ensure AnyswapTracker is up and running.
2. Configure Database.ini with the correct database connection parameters
3. Save the bot API key to telegramapi.txt.
The program needs to run continously in the background. 
# FAQ
Anyswap rewards you for providing liquidity in a similar way to staking a coin in a staking pool. The staked coin, however, in the case of Anyswap, is a special kind of token called LP token (Liquidity Pool Token). When you provide liquidity to Anyswap, you are buying LP tokens with an initial price of 50% of each of the two underlying assets.
For example: if you pooled 1000$ in the FSN-ANY pool, you are buying 500$ in Fusion and 500$ in Any and exchanging these for FSN-ANY LP tokens.

## Q1. How am I getting rewarded for providing liquidity?
Two ways:
1. ANY rewards: every 24 hours, ANY rewards are distributed for all people providing liquidity on Anyswap.
2. Pool fees: for every trade, 0.3% of the trade value goes back to the pool, meaning your share increase with every trade.
## Q2. Ok. so how are the rewards calculated?
The rewards are calculated compared to providing liquidity with zero trading fees and no ANY rewards. Of course, it makes no sense to provide liquidity with zero rewards, but this happens, for example, if you provided liquidity on uniswap for a pool with zero trading volume.
### Examples:
1. ANY rewards: when APY shows 50% ANY, it means that:
"If you sold all ANY you accumulated for the entire year, and bought back into liquidity pool, you will end up with 50% more LP tokens that what you started with"
2. Pool fees: when APY shows 50%, it means that:
"If you stayed in the pool for the entire year, your LP token now is worth 50% more than your initial purchase (See next question)"
Note how the rewards are a little different: You are getting more LP tokens for any rewards. But for pool fees, your number of LP tokens stays the same, but their value increases.
## But I am getting less than the calculation shows?
Two reasons:
1. The calculation is measured in LP token value, not in USD. If both assets in the Liquidity Pool dropped in USD value, then the LP token value will also drop in USD.  You will end up with less USD, but more of the underlying assets you are pooling.
Also, if one coin dropped significantly in value compared to the other, then you are
 subjected to what's called "Impermanent Loss." Impermanent Loss is temporary as long
  as the price ratio between the underlying assets is the same at the time of your
   entry and exit. Check [The beginner's guide to
 Impermanent Loss](https://blog.bancor.network/beginners-guide-to-getting-rekt-by-impermanent-loss-7c9510cb2f22)

## I am getting More than the calculation shows?
If you invest whatever you earned in ANY rewards back in the pool, you are compounding your returns.
* Assuming ANY value stays the same. If ANY value grows too much, it will be better if you didn't invest it back.
## What are the risks of providing liquidity?
1. if you are not comfortable with exposure to both assets of the pool, then providing liquidity is not for you. For example, you might end up with double your initial investment in terms of both coins, but less than what you started with, as measured in USD
2. Impermanent Loss: if one coin dropped significantly in value compared to the other, then you are subjected to what's called to Impermanent Loss. Impermanent Loss is temporary as long as the price ratio between the underlying assets is the same at the time of your entry and exit. [The beginner's guide to
 Impermanent Loss](https://blog.bancor.network/beginners-guide-to-getting-rekt-by-impermanent-loss-7c9510cb2f22)
