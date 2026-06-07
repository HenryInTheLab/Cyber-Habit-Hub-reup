<template>
  <div class="about-page">
    <div class="page-content">
      <div class="page-header">
        <div class="container">
          <h1 class="page-title">About CyberHabit Hub</h1>
          <p class="page-subtitle">Empowering Digital Citizens Through Cybersecurity Education and Support</p>
        </div>
      </div>

      <div class="container">
        <div class="page-body">
          <div class="about-section">
            <h2>Our Mission</h2>
            <p>At CyberHabit Hub, we believe that cybersecurity education should be accessible, engaging, and empowering for everyone. Our mission is to foster digital citizenship by providing comprehensive cybersecurity education, practical tools, and support resources that help individuals and communities navigate the digital world safely and confidently.</p>
          </div>

          <div class="about-section">
            <h2>What We Do</h2>
            <div class="grid">
              <div class="card">
                <h3>Educational Resources</h3>
                <ul>
                  <li>Interactive cybersecurity challenges</li>
                  <li>Comprehensive learning materials</li>
                  <li>Real-world case studies</li>
                  <li>Expert-curated content</li>
                </ul>
              </div>
              <div class="card">
                <h3>Practical Tools</h3>
                <ul>
                  <li>Link safety checker</li>
                  <li>Security assessment tools</li>
                  <li>Privacy protection guides</li>
                  <li>Digital hygiene checklists</li>
                </ul>
              </div>
              <div class="card">
                <h3>Community Support</h3>
                <ul>
                  <li>Peer learning networks</li>
                  <li>Expert Q&A sessions</li>
                  <li>Support forums</li>
                  <li>Recovery assistance</li>
                </ul>
              </div>
              <div class="card">
                <h3>Research & Insights</h3>
                <ul>
                  <li>Cybersecurity trend analysis</li>
                  <li>Threat intelligence reports</li>
                  <li>Educational impact studies</li>
                  <li>Best practice recommendations</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="about-section">
            <h2>Our Values</h2>
            <div class="values-grid">
              <div class="value-item">
                <h3>Accessibility</h3>
                <p>We believe cybersecurity education should be available to everyone, regardless of technical background or experience level.</p>
              </div>
              <div class="value-item">
                <h3>Empowerment</h3>
                <p>Our goal is to equip users with the knowledge and tools they need to protect themselves and make informed decisions online.</p>
              </div>
              <div class="value-item">
                <h3>Community</h3>
                <p>We foster a supportive community where users can learn together, share experiences, and help each other stay safe online.</p>
              </div>
              <div class="value-item">
                <h3>Innovation</h3>
                <p>We continuously evolve our platform and content to address emerging threats and educational needs in cybersecurity.</p>
              </div>
            </div>
          </div>

          <div class="about-section">
            <h2>Our Team</h2>
            <p>CyberHabit Hub is developed by Prism Sync, a dedicated team of cybersecurity experts, educators, and developers committed to making the digital world safer for everyone. Our diverse team brings together decades of experience in:</p>
            <ul class="team-skills">
              <li>Cybersecurity research and analysis</li>
              <li>Educational technology and curriculum design</li>
              <li>Software development and user experience design</li>
              <li>Community outreach and support services</li>
              <li>Digital forensics and incident response</li>
            </ul>
          </div>

          <div class="about-section">
            <h2>Our Impact</h2>
            <div class="impact-stats">
              <div class="stat-item">
                <h3>20+</h3>
                <p>Users Educated</p>
              </div>
              <div class="stat-item">
                <h3>50+</h3>
                <p>Cybersecurity Challenges Completed</p>
              </div>
              <div class="stat-item">
                <h3>95%</h3>
                <p>User Satisfaction Rate</p>
              </div>
              <div class="stat-item">
                <h3>24/7</h3>
                <p>Support Available</p>
              </div>
            </div>
          </div>

          <div class="about-section">
            <h2>Get Involved</h2>
            <p>Join our mission to create a safer digital world. Whether you're looking to learn, contribute, or collaborate, there are many ways to get involved with CyberHabit Hub:</p>
            <div class="involvement-grid">
              <div class="involvement-card">
                <h3>For Learners</h3>
                <ul>
                  <li>Complete cybersecurity challenges</li>
                  <li>Access our learning library</li>
                  <li>Join community discussions</li>
                  <li>Track your progress</li>
                </ul>
              </div>
              <div class="involvement-card">
                <h3>For Educators</h3>
                <ul>
                  <li>Use our curriculum materials</li>
                  <li>Create custom challenges</li>
                  <li>Access teaching resources</li>
                  <li>Connect with other educators</li>
                </ul>
              </div>
              <div class="involvement-card">
                <h3>For Organizations</h3>
                <ul>
                  <li>Implement cybersecurity training</li>
                  <li>Access enterprise features</li>
                  <li>Customize learning paths</li>
                  <li>Get dedicated support</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="about-section quote">
            <h2>Together, We Build a Safer Digital Future</h2>
            <p>"Cybersecurity is not just about technology—it's about people, education, and community. At CyberHabit Hub, we're committed to empowering every digital citizen with the knowledge and tools they need to thrive safely online."</p>
          </div>
        </div>
      </div>
    </div>
    <FooterSection />
  </div>
</template>

<script>
import FooterSection from '../section/HomePage/FooterSection.vue'

export default {
  name: 'AboutUsPage',
  components: {
    FooterSection
  }
}
</script>

<style scoped>
.about-page {
  background: var(--violet-dark);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.page-header {
  background: var(--violet-dark);
  color: var(--text-light);
  padding: 4rem 0;
  text-align: center;
}

.page-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px var(--shadow-dark);
}

.page-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  max-width: 1000px;
  margin: 0 auto;
}

.container {
  max-width: 1200px;
}

.page-body {
  background: var(--violet-light);
  border-radius: 12px;
  padding: 3rem;
  margin-bottom: 4rem;
  flex: 1;
}

.about-section {
  background: var(--violet-light);
  padding: 2rem 2rem 1rem;
}

.about-section h2 {
  color: var(--text-primary);
  font-size: 2rem;
  font-weight: 600;
  border-bottom: 3px solid var(--border-medium);
  margin-bottom: 1.5rem;
}

.about-section p {
  color: var(--text-secondary);
  font-size: 1.25rem;
  font-weight: 500;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.card {
  background: white;
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 1rem 1.25rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card h3 {
  display: flex;
  align-items: center;
  font-weight: 600;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-light);
  padding-bottom: 0.4rem;
}

.card ul {
  padding-left: 1rem;
  color: var(--text-secondary);
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
}

.value-item {
  background: white;
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 1.5rem;
  text-align: center;
}

.value-item h3 {
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.value-item p {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 0;
}

.team-skills {
  padding-left: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.impact-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.stat-item {
  background: white;
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 1.5rem;
  text-align: center;
}

.stat-item h3 {
  color: var(--violet-dark);
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-item p {
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0;
}

.involvement-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.involvement-card {
  background: white;
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 1.5rem;
}

.involvement-card h3 {
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  border-bottom: 2px solid var(--violet-dark);
  padding-bottom: 0.5rem;
}

.involvement-card ul {
  padding-left: 1rem;
  color: var(--text-secondary);
}

.quote {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
}

.quote h2 {
  border-bottom: none;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .grid {
    grid-template-columns: 1fr;
  }

  .values-grid {
    grid-template-columns: 1fr;
  }

  .impact-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .involvement-grid {
    grid-template-columns: 1fr;
  }

  .about-section {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 2.5rem;
  }

  .page-subtitle {
    font-size: 1.1rem;
  }
}
</style>
