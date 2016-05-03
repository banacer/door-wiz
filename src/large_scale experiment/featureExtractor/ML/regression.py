import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model


arr = np.genfromtxt('measurements.dat', delimiter=',')
X_train = arr[:,np.newaxis,1]
Y_train = arr[:,np.newaxis,0]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train, Y_train)

# The coefficients
print('Coefficients: ', regr.coef_)

# Plot outputs
plt.scatter(X_train, Y_train,  color='black')
plt.plot(X_train, regr.predict(X_train), color='blue',
         linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()