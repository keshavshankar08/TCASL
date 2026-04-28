#!/bin/bash
set -e 

echo "🚀 Building TCASL for macOS..."
python3 build.py

echo "📦 Setting up DMG staging area..."
rm -rf dmg_staging
mkdir -p dmg_staging

echo "📋 Copying app to staging..."
cp -R dist/TCASL.app dmg_staging/

echo "🔗 Creating Applications symlink..."
ln -s /Applications dmg_staging/Applications

echo "💿 Creating TCASL.dmg..."
hdiutil create -volname "TCASL" -srcfolder dmg_staging -ov -format UDZO TCASL.dmg

echo "🧹 Cleaning up..."
rm -rf dmg_staging

echo "✅ Done! TCASL.dmg is ready."