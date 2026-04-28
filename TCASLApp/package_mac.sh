#!/bin/bash

echo "🚀 Building TCASL for macOS..."
python3 build.py

echo "📦 Setting up DMG staging area..."
# Remove old staging if it exists, then create a fresh one
rm -rf dmg_staging
mkdir -p dmg_staging

echo "📋 Copying app to staging..."
cp -R dist/TCASL.app dmg_staging/

echo "🔗 Creating Applications symlink..."
ln -s /Applications dmg_staging/Applications

echo "💿 Creating TCASL.dmg..."
hdiutil create -volname "TCASL" -srcfolder dmg_staging -ov -format UDZO TCASL.dmg

echo "🧹 Cleaning up staging folder..."
rm -rf dmg_staging

echo "✅ Done! TCASL.dmg is ready in your folder to be uploaded to GitHub."