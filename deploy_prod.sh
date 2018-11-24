mkdir api
git ls-files api | xargs cp api
# scp -r frontend/dist/* api .htaccess $1@athena.dialup.mit.edu:/afs/athena.mit.edu/activity/c/crossp/web_scripts/s2
# rm -r api
