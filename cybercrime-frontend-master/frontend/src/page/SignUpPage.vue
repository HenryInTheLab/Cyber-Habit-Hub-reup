<template>
  <div class="signup-container">
    <div class="signup-card">

      <!-- Step 1: 2FA Setup and QR Code -->
      <div v-if="currentStep === 1" class="step-content">
        <h2 class="step-title">Create New Account</h2>
        <p class="step-description">1. Please download Google Authenticator</p>

        <div class="totp-setup">
          <!-- Download Links -->
          <div class="download-prompt">
            <div class="download-links">
              <a href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2" target="_blank" class="download-link">
                <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Get it on Google Play" />
              </a>
              <a href="https://apps.apple.com/app/google-authenticator/id388497605" target="_blank" class="download-link">
                <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Download_on_the_App_Store_Badge.svg" alt="Download on the App Store" />
              </a>
            </div>
          </div>

          <!-- QR Code -->
          <p class="step-description">2. Scan the QR code</p>
          <div class="qr-section">
            <div class="qr-container">
              <canvas ref="qrCanvas" class="qr-code"></canvas>
            </div>
          </div>

          <!-- Manual Input -->
          <div class="manual-input" v-if="signupResponse?.totp_secret">
            <p class="step-description">Or Enter The Secret Code Manually</p>
            <div class="secret-container">
              <code class="secret-code">{{ signupResponse.totp_secret }}</code>
              <button @click="copyTOTPSecret" class="btn-secondary btn-small">Copy</button>
            </div>
          </div>

          <div v-if="errors.signup" class="error-message">
            {{ errors.signup }}
          </div>

          <div class="next-step" v-if="canProceedToVerification">
            <button @click="nextStep" class="btn-primary">
              Next
            </button>
          </div>
        </div>
      </div>


      <!-- Step 2: Verification Code Input -->
      <div v-if="currentStep === 2" class="step-content">
        <!-- 用户欢迎信息 -->
        <div v-if="signupResponse?.username" class="user-welcome">
          <p class="welcome-text">Welcome, <span class="username">{{ signupResponse.username }}</span>!</p>
        </div>
        <h2 class="step-title">Enter Verification Code</h2>
        <p class="step-description">Please enter the 6-digit verification code from Google Authenticator</p>
        <div class="verification-form">
          <div class="code-input-container">
            <input
              v-model="verificationCode"
              @input="handleVerificationCodeInput"
              type="text"
              placeholder="000000"
              maxlength="6"
              class="code-input"
              :disabled="isVerifying"
            />
          </div>

          <div v-if="errors.verification" class="error-message">
            {{ errors.verification }}
          </div>

          <div class="verification-actions">
            <button @click="previousStep" class="btn-secondary">Previous</button>
            <button
              @click="verifyTOTPCode"
              class="btn-primary"
              :disabled="!isValidVerificationCode || isVerifying"
            >
              <span v-if="isVerifying">Verifying...</span>
              <span v-else>Verify and Continue</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Step 3: Recovery Phrase -->
      <div v-if="currentStep === 3" class="step-content">
        <h2 class="step-title">Registration Complete!</h2>
        <p class="step-description">✅ Your account has been successfully created. Please save the recovery phrase in a secure location and do not share it with others.</p>

        <div class="recovery-phrase-section">
          <div class="phrase-container">
            <div class="phrase-words">
              <div
                v-for="(word, index) in recoveryWords"
                :key="index"
                class="phrase-word"
              >
                {{ index + 1 }}. {{ word }}
              </div>
            </div>
            <button @click="copyRecoveryPhrase" class="btn-secondary">Copy Recovery Phrase</button>
          </div>

          <div class="completion-actions">
            <button @click="previousStep" class="btn-secondary">Previous</button>
            <button @click="completeSignup" class="btn-primary">
              Go to User Center
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'SignUp',
  data() {
    return {
      // Current step: 1-Scan QR Code, 2-Enter Code, 3-Recovery Phrase
      currentStep: 1,

      // Registration data returned from API
      signupResponse: null,

      // 6-digit verification code entered by user
      verificationCode: '',

      // State control
      isVerifying: false,

      // Error messages
      errors: {
        signup: '',
        verification: ''
      }
    }
  },

  computed: {
    // Split recovery phrase into word array
    recoveryWords() {
      if (!this.signupResponse?.recovery_phrase) return []
      return this.signupResponse.recovery_phrase.split(' ')
    },

    // Check if verification step can proceed
    canProceedToVerification() {
      return this.signupResponse &&
             this.signupResponse.otp_uri &&
             this.signupResponse.totp_secret
    },

    // Check if verification code is valid (6 digits)
    isValidVerificationCode() {
      return /^\d{6}$/.test(this.verificationCode)
    }
  },

  methods: {
    // Step 1: Call registration API to generate QR code
    async initiateSignup() {
      this.errors.signup = ''

      try {
        const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/users/signup/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({}) // Empty body, backend auto-generates username
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || 'Registration failed')
        }

        // Save data returned from API
        this.signupResponse = await response.json()

        // Generate QR code
        await this.generateQRCode()

        console.log('Signup initiated successfully:', {
          username: this.signupResponse.username,
          hasOtpUri: !!this.signupResponse.otp_uri,
          hasSecret: !!this.signupResponse.totp_secret,
          hasRecoveryPhrase: !!this.signupResponse.recovery_phrase
        })

      } catch (error) {
        console.error('Signup failed:', error)
        this.errors.signup = error.message
      }
    },

    // Generate QR code
    async generateQRCode() {
      if (!this.signupResponse?.otp_uri) return

      try {
        const canvas = this.$refs.qrCanvas
        if (canvas) {
          await QRCode.toCanvas(canvas, this.signupResponse.otp_uri, {
            width: 150,
            margin: 2
          })
        }
      } catch (error) {
        console.error('QR code generation failed:', error)
      }
    },

    // Go to next step
    nextStep() {
      if (this.currentStep === 1 && this.canProceedToVerification) {
        this.currentStep = 2
      }
    },

    // Handle verification code input
    handleVerificationCodeInput() {
      // Only allow digits, maximum 6 digits
      this.verificationCode = this.verificationCode.replace(/\D/g, '').slice(0, 6)
      this.errors.verification = ''
    },

    // Verify TOTP code using the new verify API
    async verifyTOTPCode() {
      if (!this.isValidVerificationCode) return

      this.isVerifying = true
      this.errors.verification = ''

      try {
        console.log('Verifying TOTP code:', this.verificationCode)

        // Call the new verify API
        const response = await fetch('https://godo2xgjc9.execute-api.ap-southeast-2.amazonaws.com/users/verify/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            totp_secret: this.signupResponse.totp_secret,
            username: this.signupResponse.username,
            code: this.verificationCode,
            recovery_phrase: this.signupResponse.recovery_phrase
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || 'Verification failed')
        }

        // Save the verification response (contains user info and tokens)
        const verifyResponse = await response.json()
        this.signupResponse.verifyResponse = verifyResponse

        console.log('TOTP verification successful:', verifyResponse)

        // Proceed to recovery phrase step
        this.currentStep = 3

      } catch (error) {
        console.error('TOTP verification failed:', error)
        this.errors.verification = error.message || 'Invalid verification code, please try again'
      } finally {
        this.isVerifying = false
      }
    },

    // Copy to clipboard
    async copyToClipboard(text) {
      try {
        await navigator.clipboard.writeText(text)
        // Simple success notification
        alert('Copied to clipboard!')
      } catch (error) {
        console.error('Failed to copy to clipboard:', error)
        // Fallback: create temporary input field
        this.fallbackCopyToClipboard(text)
      }
    },

    // Fallback copy method
    fallbackCopyToClipboard(text) {
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.select()
      try {
        document.execCommand('copy')
        alert('Copied to clipboard!')
      } catch (err) {
        console.error('Fallback copy failed:', err)
      }
      document.body.removeChild(textArea)
    },

    // Copy TOTP secret
    async copyTOTPSecret() {
      if (this.signupResponse?.totp_secret) {
        await this.copyToClipboard(this.signupResponse.totp_secret)
      }
    },

    // Copy recovery phrase
    async copyRecoveryPhrase() {
      if (this.signupResponse?.recovery_phrase) {
        await this.copyToClipboard(this.signupResponse.recovery_phrase)
      }
    },

    // Complete registration using verify API response
    async completeSignup() {
      console.log('Signup completed successfully')

      try {
        // Use the verify response that was saved during verification
        const verifyResponse = this.signupResponse.verifyResponse

        if (!verifyResponse) {
          throw new Error('No verification response available')
        }

        // Save tokens and user info from verify response
        if (verifyResponse.access_token) {
          localStorage.setItem('access_token', verifyResponse.access_token)
        }
        if (verifyResponse.refresh_token) {
          localStorage.setItem('refresh_token', verifyResponse.refresh_token)
        }
        if (verifyResponse.user) {
          localStorage.setItem('user_info', JSON.stringify(verifyResponse.user))
        }

        console.log('User registration and login completed:', verifyResponse)

        // Redirect to user center
        this.$router.push('/user-center')

      } catch (error) {
        console.error('Signup completion failed:', error)
        // If completion fails, redirect to login page
        this.$router.push('/signin')
      }
    },

    previousStep() {
      if (this.currentStep > 1) {
        this.currentStep--
      }
    },

    resetForm() {
      this.signupResponse = null
      this.verificationCode = ''
      this.currentStep = 1
      this.isVerifying = false
      this.errors = {
        signup: '',
        verification: ''
      }
    }
  },

  mounted() {
    console.log('SignUp component mounted')

    this.initiateSignup()
  },


  beforeUnmount() {
    console.log('SignUp component unmounting')
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--violet-ultra-dark);
  padding: 20px;
}

.signup-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  max-width: 800px;
  width: 100%;
}

.step-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  text-align: center;
}

.step-description {
  color: #666;
  margin-bottom: 8px;
  text-align: center;
}




.btn-primary, .btn-secondary {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: var(--violet-dark);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--violet-deep);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: var(--violet-light);
  color: #666;
  border: 2px solid var(--violet-light);
}

.btn-secondary:hover {
  background: var(--violet-light);
}

.btn-small {
  padding: 8px 16px;
  font-size: 16px;
}

.totp-setup {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.download-prompt {
  text-align: center;
  padding: 10px;
}


.download-links {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 8px;
}

.download-link img {
  height: 40px;
}

.qr-section {
  display: flex;
  justify-content: center;
  align-items: center;
}

.qr-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}


.qr-code {
  border: 2px solid var(--violet-light);
  border-radius: 8px;
}

.manual-input {
  display: flex;
  flex-direction: column;

}

.secret-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.secret-code {
  background: var(--violet-light);
  padding: 8px 12px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
  flex: 1;
  word-break: break-all;
  text-align: center;
}

.verification-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.code-input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.code-input {
  font-size: 24px;
  text-align: center;
  letter-spacing: 8px;
  padding: 16px;
  width: 200px;
  border: 2px solid var(--violet-light);
  border-radius: 8px;
}

.code-input:focus {
  outline: none;
  border-color: var(--violet-medium);
}

.verification-actions {
  display: flex;
  gap: 16px;
}

.recovery-phrase-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.phrase-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.phrase-words {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 20px;
  background: var(--violet-sage);
  border-radius: 8px;
  border: 2px solid var(--violet-light);
}

.phrase-word {
  padding: 8px 12px;
  background: white;
  border-radius: 4px;
  font-family: monospace;
  font-size: 16px;
  border: 1px solid var(--violet-light);
}

.completion-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.next-step {
  display: flex;
  justify-content: center;
}

.error-message {
  color: var(--violet-dark);
  background: var(--violet-light);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--violet-light);
  text-align: center;
}

/* 用户欢迎信息 */
.user-welcome {
  margin: 20px auto;
  padding: 16px 0;
  border-bottom: 3px solid var(--violet-sage);
  text-align: center;
  width: 500px;
}

.welcome-text {
  font-size: 18px;
  color: var(--violet-dark);
  margin: 0;
  font-weight: 500;
}

.username {
  font-weight: 700;
  color: var(--violet-deep);
}

@media (max-width: 768px) {
  .signup-card {
    padding: 20px;
    margin: 10px;
  }

  .qr-section {
    flex-direction: column;
    align-items: center;
  }

  .download-links {
    flex-direction: column;
    align-items: center;
  }

  .phrase-words {
    grid-template-columns: 1fr;
  }

  .verification-actions,
  .completion-actions {
    flex-direction: column;
  }

  .user-welcome {
    margin: 15px 0;
    padding: 12px;
  }

  .welcome-text {
    font-size: 16px;
  }
}
</style>
