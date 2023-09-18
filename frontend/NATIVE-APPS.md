# Generating native apps with capacitor

## Prerequisites

1. rename `capacitor.config.json.example` to `capacitor.config.json`
   1. change values to your liking
2. run `brew install cocoapods` on mac

## add ios and android apps to project

```sh
npx cap add ios
npx cap add android
```

## run apps

```sh
npx cap run ios
npx cap run android
```

## open android studio / xcode

```sh
npx cap open ios
npx cap open android
```
